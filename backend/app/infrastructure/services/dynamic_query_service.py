import logging
import os
from typing import Dict, Any, List, Optional
from openai import OpenAI
import clickhouse_connect
from urllib.parse import urlparse
import json
import instructor

from app.domain.entities.llm_models import SQLQueryResponse

logger = logging.getLogger("dynamic_query_service")


class DynamicQueryService:
    """
    Service that allows AI to generate and execute dynamic SQL queries
    against the ClickHouse database for real-time data access.
    """

    def __init__(self):
        """Initialize the dynamic query service"""
        self.clickhouse_url = os.getenv(
            "CLICKHOUSE_URL", "clickhouse://clickhouse:8123/default")
        self.client = None
        self.openai_client = None
        self._connect()
        self._init_openai()

    def _connect(self):
        """Establish connection to ClickHouse"""
        try:
            parsed = urlparse(self.clickhouse_url)
            host = parsed.hostname or "clickhouse"
            port = parsed.port or 8123
            database = parsed.path.lstrip("/") or "default"
            username = parsed.username or "default"
            password = parsed.password or ""

            self.client = clickhouse_connect.get_client(
                host=host,
                port=port,
                database=database,
                username=username,
                password=password
            )
            logger.info(f"Connected to ClickHouse for dynamic queries")
        except Exception as e:
            logger.error(f"Failed to connect to ClickHouse: {e}")
            raise

    def _init_openai(self):
        """Initialize OpenAI client for SQL generation with Instructor"""
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.openai_client = OpenAI(api_key=api_key)
            # Initialize Instructor client for structured SQL generation
            self.instructor_client = instructor.patch(self.openai_client)
        else:
            logger.warning("OPENAI_API_KEY not found for dynamic queries")
            self.openai_client = None
            self.instructor_client = None

    def get_database_schema(self) -> str:
        """Get comprehensive database schema information for SQL generation"""
        try:
            # Get table schemas - ClickHouse system.columns structure
            tables_query = """
            SELECT 
                table,
                name,
                type
            FROM system.columns 
            WHERE database = 'default'
            ORDER BY table, position
            """

            result = self.client.query(tables_query)
            schema_info = {}

            for row in result.result_rows:
                table_name = row[0]
                column_name = row[1]
                data_type = row[2]

                if table_name not in schema_info:
                    schema_info[table_name] = []
                schema_info[table_name].append(f"{column_name} ({data_type})")

            # Format comprehensive schema for AI
            schema_text = "COMPREHENSIVE DATABASE SCHEMA:\n"
            schema_text += "=" * 50 + "\n\n"

            for table, columns in schema_info.items():
                schema_text += f"TABLE: {table}\n"
                schema_text += "-" * 30 + "\n"
                schema_text += "COLUMNS:\n"
                for column in columns:
                    schema_text += f"  - {column}\n"
                schema_text += "\n"

            # Add common query patterns
            schema_text += "COMMON QUERY PATTERNS:\n"
            schema_text += "=" * 30 + "\n"
            schema_text += """
1. For sales analysis:
   SELECT product, SUM(revenue) as total_revenue 
   FROM sales_data 
   WHERE date >= today() - 7 
   GROUP BY product 
   ORDER BY total_revenue DESC 
   LIMIT 5

2. For store performance:
   SELECT store, SUM(revenue) as store_revenue, SUM(profit) as store_profit 
   FROM sales_data 
   WHERE date >= today() - 30 
   GROUP BY store 
   ORDER BY store_revenue DESC

3. For product trends:
   SELECT date, product, SUM(quantity_sold) as total_quantity 
   FROM sales_data 
   WHERE date >= today() - 30 
   GROUP BY date, product 
   ORDER BY date DESC

4. For profit analysis:
   SELECT product, SUM(revenue) as total_revenue, SUM(profit) as total_profit,
          (SUM(profit) / SUM(revenue) * 100) as profit_margin 
   FROM sales_data 
   WHERE date >= today() - 7 
   GROUP BY product 
   HAVING total_revenue > 0 
   ORDER BY profit_margin DESC
"""

            return schema_text

        except Exception as e:
            logger.error(f"Error getting database schema: {e}")
            return "DATABASE SCHEMA: Unable to retrieve schema information"

    def generate_sql_query(self, user_query: str) -> str:
        """Generate SQL query based on user's natural language query using Instructor"""
        if not self.instructor_client:
            logger.warning(
                "Instructor client not available for SQL generation")
            return None

        try:
            schema = self.get_database_schema()

            # Use Instructor for structured SQL generation
            sql_response: SQLQueryResponse = self.instructor_client.chat.completions.create(
                model="gpt-4o",
                response_model=SQLQueryResponse,
                messages=[
                    {
                        "role": "system",
                        "content": """You are a ClickHouse SQL expert. Generate accurate SQL queries based on natural language questions.

                        CRITICAL RULES:
                        1. ONLY use the tables listed in the schema (sales_data, customer_data, inventory_data, etc.)
                        2. ONLY generate SELECT queries (no INSERT, UPDATE, DELETE)
                        3. Use ClickHouse syntax and functions
                        4. Always include LIMIT clause for large result sets
                        5. Use proper aggregation functions (SUM, COUNT, AVG, etc.)
                        6. Use table aliases for readability
                        7. Handle dates with proper ClickHouse date functions (today(), toDate(), etc.)
                        8. Do NOT reference tables that don't exist in the schema
                        9. Use the exact column names from the schema
                        10. Always set safety_check to True for SELECT queries
                        
                        AVAILABLE TABLES: sales_data, customer_data, inventory_data, daily_metrics_mv, product_performance_mv, store_performance_mv
                        """
                    },
                    {
                        "role": "user",
                        "content": f"""
                        {schema}
                        
                        Generate a ClickHouse SQL query for this question: "{user_query}"
                        
                        IMPORTANT: 
                        - Only use tables and columns that exist in the schema above
                        - Provide a clear explanation of what the query does
                        - List all tables and columns used in the query
                        - Ensure the query is safe (SELECT only)
                        """
                    }
                ],
                temperature=0.1,
                max_tokens=800
            )

            # Validate the generated query
            if not sql_response.safety_check:
                logger.warning("Generated query failed safety check")
                return None

            if not sql_response.sql_query.strip().upper().startswith("SELECT"):
                logger.warning("Generated query is not a SELECT statement")
                return None

            logger.info(f"Generated SQL query: {sql_response.sql_query}")
            logger.info(f"Query type: {sql_response.query_type}")
            logger.info(f"Tables used: {sql_response.tables_used}")
            logger.info(f"Explanation: {sql_response.explanation}")

            return sql_response.sql_query

        except Exception as e:
            logger.error(f"Error generating SQL query with Instructor: {e}")
            return None

    def execute_query(self, sql_query: str) -> Dict[str, Any]:
        """Execute SQL query and return results"""
        try:
            if not sql_query:
                return {"error": "No SQL query provided"}

            # Add safety check - only allow SELECT queries
            if not sql_query.strip().upper().startswith("SELECT"):
                return {"error": "Only SELECT queries are allowed"}

            result = self.client.query(sql_query)

            # Convert results to structured format
            columns = [desc[0] for desc in result.column_names]
            rows = []

            for row in result.result_rows:
                row_dict = {}
                for i, value in enumerate(row):
                    # Handle different data types
                    if hasattr(value, 'isoformat'):  # datetime objects
                        row_dict[columns[i]] = value.isoformat()
                    else:
                        row_dict[columns[i]] = value
                rows.append(row_dict)

            return {
                "success": True,
                "columns": columns,
                "rows": rows,
                "row_count": len(rows),
                "sql_query": sql_query
            }

        except Exception as e:
            logger.error(f"Error executing SQL query: {e}")
            return {
                "success": False,
                "error": str(e),
                "sql_query": sql_query
            }

    def query_database_directly(self, user_query: str) -> Dict[str, Any]:
        """Main method: Generate SQL from user query and execute it"""
        try:
            # Step 1: Generate SQL query
            sql_query = self.generate_sql_query(user_query)
            if not sql_query:
                return {"error": "Failed to generate SQL query"}

            # Step 2: Execute the query
            result = self.execute_query(sql_query)

            # Step 3: Add metadata
            result["user_query"] = user_query
            result["query_type"] = "dynamic_sql"

            return result

        except Exception as e:
            logger.error(f"Error in dynamic query process: {e}")
            return {"error": f"Dynamic query failed: {str(e)}"}

    def get_sample_data(self, table_name: str, limit: int = 5) -> Dict[str, Any]:
        """Get sample data from a specific table"""
        try:
            sql_query = f"SELECT * FROM {table_name} LIMIT {limit}"
            return self.execute_query(sql_query)
        except Exception as e:
            logger.error(f"Error getting sample data: {e}")
            return {"error": str(e)}

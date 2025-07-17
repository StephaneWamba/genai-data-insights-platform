import os
from typing import List, Dict, Any
import clickhouse_connect
from datetime import datetime, timedelta
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class RealDataService:
    """
    Service for querying real business data from ClickHouse data warehouse.
    Provides sales, inventory, and customer data from the modern data stack.
    """

    def __init__(self):
        """Initialize the real data service with ClickHouse connection"""
        self.clickhouse_url = os.getenv(
            "CLICKHOUSE_URL", "clickhouse://clickhouse:8123/default")
        self.client = None
        self._connect()

    def _connect(self):
        """Establish connection to ClickHouse using robust URL parsing"""
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
            logger.info(
                f"Connected to ClickHouse at {host}:{port}/{database} as {username}")
        except Exception as e:
            logger.error(f"Failed to connect to ClickHouse: {e}")
            raise

    def get_sales_data(self, days: int = 30) -> List[Dict[str, Any]]:
        """
        Retrieve sales data from ClickHouse for the specified number of days.

        Args:
            days: Number of days of data to retrieve

        Returns:
            List of sales records
        """
        try:
            query = f"""
            SELECT 
                date,
                product,
                category,
                store,
                quantity_sold,
                revenue,
                profit
            FROM sales_data 
            WHERE date >= today() - INTERVAL {days} DAY
            ORDER BY date DESC
            """

            result = self.client.query(query)
            sales_data = []

            for row in result.result_rows:
                sales_data.append({
                    "date": row[0].strftime("%Y-%m-%d") if row[0] else None,
                    "product": row[1],
                    "category": row[2],
                    "store": row[3],
                    "quantity_sold": row[4],
                    "revenue": float(row[5]) if row[5] else 0.0,
                    "profit": float(row[6]) if row[6] else 0.0
                })

            logger.info(
                f"Retrieved {len(sales_data)} sales records for {days} days")
            return sales_data

        except Exception as e:
            logger.error(f"Error retrieving sales data: {e}")
            # Fallback to empty data
            return []

    def get_customer_data(self, count: int = 100) -> List[Dict[str, Any]]:
        """
        Retrieve customer data from ClickHouse.

        Args:
            count: Number of customers to retrieve

        Returns:
            List of customer records
        """
        try:
            query = f"""
            SELECT 
                customer_id,
                name,
                email,
                age_group,
                total_purchases,
                last_purchase,
                preferred_store,
                region
            FROM customer_data 
            LIMIT {count}
            """

            result = self.client.query(query)
            customer_data = []

            for row in result.result_rows:
                customer_data.append({
                    "customer_id": row[0],
                    "name": row[1],
                    "email": row[2],
                    "age_group": row[3],
                    "total_purchases": float(row[4]) if row[4] else 0.0,
                    "last_purchase": row[5].strftime("%Y-%m-%d") if row[5] else None,
                    "preferred_store": row[6],
                    "region": row[7]
                })

            logger.info(f"Retrieved {len(customer_data)} customer records")
            return customer_data

        except Exception as e:
            logger.error(f"Error retrieving customer data: {e}")
            # Fallback to empty data
            return []

    def get_inventory_data(self) -> List[Dict[str, Any]]:
        """
        Retrieve current inventory data from ClickHouse.

        Returns:
            List of inventory records
        """
        try:
            query = """
            SELECT 
                product,
                store,
                current_stock,
                reorder_level,
                supplier
            FROM inventory_data 
            ORDER BY store, product
            """

            result = self.client.query(query)
            inventory_data = []

            for row in result.result_rows:
                inventory_data.append({
                    "product": row[0],
                    "store": row[1],
                    "current_stock": row[2],
                    "reorder_level": row[3],
                    "supplier": row[4]
                })

            logger.info(f"Retrieved {len(inventory_data)} inventory records")
            return inventory_data

        except Exception as e:
            logger.error(f"Error retrieving inventory data: {e}")
            # Fallback to empty data
            return []

    def get_business_metrics(self) -> Dict[str, Any]:
        """
        Calculate key business metrics from ClickHouse data.

        Returns:
            Dictionary of business metrics
        """
        try:
            # Get sales data for calculations
            sales_data = self.get_sales_data(30)

            if not sales_data:
                return self._get_empty_metrics()

            # Calculate metrics
            total_revenue = sum(record["revenue"] for record in sales_data)
            total_profit = sum(record["profit"] for record in sales_data)
            total_sales = sum(record["quantity_sold"] for record in sales_data)

            # Store performance
            store_performance = {}
            stores = set(record["store"] for record in sales_data)
            for store in stores:
                store_sales = [r for r in sales_data if r["store"] == store]
                store_performance[store] = {
                    "revenue": sum(r["revenue"] for r in store_sales),
                    "profit": sum(r["profit"] for r in store_sales),
                    "sales_count": sum(r["quantity_sold"] for r in store_sales)
                }

            # Product performance
            product_performance = {}
            products = set(record["product"] for record in sales_data)
            for product in products:
                product_sales = [
                    r for r in sales_data if r["product"] == product]
                product_performance[product] = {
                    "revenue": sum(r["revenue"] for r in product_sales),
                    "profit": sum(r["profit"] for r in product_sales),
                    "sales_count": sum(r["quantity_sold"] for r in product_sales)
                }

            return {
                "total_revenue": round(total_revenue, 2),
                "total_profit": round(total_profit, 2),
                "total_sales": total_sales,
                "profit_margin": round((total_profit / total_revenue * 100), 2) if total_revenue > 0 else 0,
                "store_performance": store_performance,
                "product_performance": product_performance,
                "generated_at": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error calculating business metrics: {e}")
            return self._get_empty_metrics()

    def search_data(self, query: str) -> Dict[str, Any]:
        """
        Search through data based on natural language query.

        Args:
            query: Natural language search query

        Returns:
            Relevant data based on the query
        """
        query_lower = query.lower()

        try:
            if "sales" in query_lower or "revenue" in query_lower:
                return {
                    "data_type": "sales",
                    "data": self.get_sales_data(7),  # Last 7 days
                    "query": query,
                    "data_sources": ["clickhouse_sales_data"]
                }
            elif "inventory" in query_lower or "stock" in query_lower:
                return {
                    "data_type": "inventory",
                    "data": self.get_inventory_data(),
                    "query": query,
                    "data_sources": ["clickhouse_inventory_data"]
                }
            elif "customer" in query_lower or "customers" in query_lower:
                return {
                    "data_type": "customers",
                    "data": self.get_customer_data(50),
                    "query": query,
                    "data_sources": ["clickhouse_customer_data"]
                }
            else:
                # Default to sales data
                return {
                    "data_type": "sales",
                    "data": self.get_sales_data(7),
                    "query": query,
                    "data_sources": ["clickhouse_sales_data"]
                }
        except Exception as e:
            logger.error(f"Error in data search: {e}")
            return {
                "data_type": "error",
                "data": [],
                "query": query,
                "error": str(e)
            }

    def _get_empty_metrics(self) -> Dict[str, Any]:
        """Return empty metrics structure when data is unavailable"""
        return {
            "total_revenue": 0,
            "total_profit": 0,
            "total_sales": 0,
            "profit_margin": 0,
            "store_performance": {},
            "product_performance": {},
            "generated_at": datetime.now().isoformat()
        }

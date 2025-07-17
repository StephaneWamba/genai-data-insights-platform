#!/usr/bin/env python3
"""
Data Ingestion Service
Populates ClickHouse data warehouse with realistic business data
"""

import os
import time
import random
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any

import clickhouse_driver
import psycopg2
from kafka import KafkaProducer
import pandas as pd
import numpy as np
from faker import Faker
import json
import schedule

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Faker for realistic data generation
fake = Faker()


class DataIngestionService:
    """Service for ingesting realistic business data into the data stack"""

    def __init__(self):
        """Initialize connections to data sources"""
        self.clickhouse_client = self._init_clickhouse()
        self.postgres_client = self._init_postgres()
        self.kafka_producer = self._init_kafka()

        # Business configuration
        self.stores = ["Paris Central", "Paris North",
                       "London Central", "London West", "Berlin Central"]
        self.products = ["Shoes", "Clothing",
                         "Accessories", "Electronics", "Home Goods"]
        self.categories = ["Footwear", "Apparel",
                           "Jewelry", "Tech", "Furniture"]
        self.regions = ["Paris", "London", "Berlin", "Other"]

    def _init_clickhouse(self) -> clickhouse_driver.Client:
        """Initialize ClickHouse connection"""
        try:
            client = clickhouse_driver.Client(
                host=os.getenv('CLICKHOUSE_HOST', 'clickhouse'),
                port=int(os.getenv('CLICKHOUSE_PORT', 9000)),
                database=os.getenv('CLICKHOUSE_DB', 'default'),
                user=os.getenv('CLICKHOUSE_USER', 'default'),
                password=os.getenv('CLICKHOUSE_PASSWORD', '')
            )
            logger.info("ClickHouse connection established")
            return client
        except Exception as e:
            logger.error(f"ClickHouse connection failed: {e}")
            return None

    def _init_postgres(self) -> psycopg2.extensions.connection:
        """Initialize PostgreSQL connection"""
        try:
            conn = psycopg2.connect(os.getenv('POSTGRES_URL'))
            logger.info("PostgreSQL connection established")
            return conn
        except Exception as e:
            logger.error(f"PostgreSQL connection failed: {e}")
            return None

    def _init_kafka(self) -> KafkaProducer:
        """Initialize Kafka producer"""
        try:
            producer = KafkaProducer(
                bootstrap_servers=os.getenv(
                    'KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092'),
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            logger.info("Kafka producer established")
            return producer
        except Exception as e:
            logger.error(f"Kafka connection failed: {e}")
            return None

    def generate_sales_data(self, days: int = 30) -> List[Dict[str, Any]]:
        """Generate realistic sales data"""
        sales_data = []
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        for i in range(days):
            current_date = start_date + timedelta(days=i)

            # Generate daily sales for each store
            for store in self.stores:
                # Base sales with some randomness
                base_sales = random.randint(50, 200)

                # Weekend effect
                if current_date.weekday() >= 5:  # Saturday/Sunday
                    base_sales = int(base_sales * 1.3)

                # Seasonal effect (higher sales in December)
                if current_date.month == 12:
                    base_sales = int(base_sales * 1.5)

                # Generate sales for each product category
                for product in self.products:
                    product_sales = random.randint(
                        5, base_sales // len(self.products))
                    revenue = product_sales * random.uniform(20, 100)
                    cost = product_sales * random.uniform(10, 50)
                    profit = revenue - cost

                    sales_record = {
                        "id": len(sales_data) + 1,
                        "date": current_date.strftime("%Y-%m-%d"),
                        "store": store,
                        "product": product,
                        "category": random.choice(self.categories),
                        "quantity_sold": product_sales,
                        "revenue": round(revenue, 2),
                        "cost": round(cost, 2),
                        "profit": round(profit, 2),
                        "region": "Paris" if "Paris" in store else "London" if "London" in store else "Berlin",
                        "created_at": current_date
                    }
                    sales_data.append(sales_record)

        return sales_data

    def generate_customer_data(self, count: int = 100) -> List[Dict[str, Any]]:
        """Generate realistic customer data"""
        customer_data = []

        for i in range(count):
            customer_record = {
                "customer_id": f"CUST_{i+1:04d}",
                "name": fake.name(),
                "email": fake.email(),
                "region": random.choice(self.regions),
                "age_group": random.choice(["18-25", "26-35", "36-45", "46-55", "55+"]),
                "total_purchases": random.randint(1, 50),
                "total_spent": round(random.uniform(50, 5000), 2),
                "last_purchase": (datetime.now() - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d"),
                "preferred_store": random.choice(self.stores),
                "preferred_category": random.choice(self.categories),
                "created_at": datetime.now()
            }
            customer_data.append(customer_record)

        return customer_data

    def generate_inventory_data(self) -> List[Dict[str, Any]]:
        """Generate inventory data"""
        inventory_data = []

        for store in self.stores:
            for product in self.products:
                current_stock = random.randint(10, 200)
                reorder_level = random.randint(5, 50)
                max_stock = random.randint(100, 300)

                inventory_record = {
                    "id": len(inventory_data) + 1,
                    "store": store,
                    "product": product,
                    "current_stock": current_stock,
                    "reorder_level": reorder_level,
                    "max_stock": max_stock,
                    "last_restocked": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
                    "supplier": f"Supplier_{random.randint(1, 5)}",
                    "status": "In Stock" if current_stock > reorder_level else "Low Stock",
                    "created_at": datetime.now()
                }
                inventory_data.append(inventory_record)

        return inventory_data

    def ingest_sales_data(self, sales_data: List[Dict[str, Any]]):
        """Ingest sales data into ClickHouse"""
        if not self.clickhouse_client:
            logger.error("ClickHouse client not available")
            return

        try:
            # Convert to ClickHouse format
            clickhouse_data = [
                (
                    record["id"],
                    record["date"],
                    record["store"],
                    record["product"],
                    record["category"],
                    record["quantity_sold"],
                    record["revenue"],
                    record["cost"],
                    record["profit"],
                    record["region"],
                    record["created_at"]
                )
                for record in sales_data
            ]

            # Insert into ClickHouse
            self.clickhouse_client.execute(
                """
                INSERT INTO sales_data 
                (id, date, store, product, category, quantity_sold, revenue, cost, profit, region, created_at)
                VALUES
                """,
                clickhouse_data
            )

            logger.info(
                f"Ingested {len(sales_data)} sales records into ClickHouse")

            # Send to Kafka for real-time processing
            if self.kafka_producer:
                for record in sales_data:
                    self.kafka_producer.send('sales_events', record)
                self.kafka_producer.flush()
                logger.info("Sent sales data to Kafka")

        except Exception as e:
            logger.error(f"Error ingesting sales data: {e}")

    def ingest_customer_data(self, customer_data: List[Dict[str, Any]]):
        """Ingest customer data into ClickHouse"""
        if not self.clickhouse_client:
            logger.error("ClickHouse client not available")
            return

        try:
            clickhouse_data = [
                (
                    record["customer_id"],
                    record["name"],
                    record["email"],
                    record["region"],
                    record["age_group"],
                    record["total_purchases"],
                    record["total_spent"],
                    record["last_purchase"],
                    record["preferred_store"],
                    record["preferred_category"],
                    record["created_at"]
                )
                for record in customer_data
            ]

            self.clickhouse_client.execute(
                """
                INSERT INTO customer_data 
                (customer_id, name, email, region, age_group, total_purchases, total_spent, 
                 last_purchase, preferred_store, preferred_category, created_at)
                VALUES
                """,
                clickhouse_data
            )

            logger.info(
                f"Ingested {len(customer_data)} customer records into ClickHouse")

        except Exception as e:
            logger.error(f"Error ingesting customer data: {e}")

    def ingest_inventory_data(self, inventory_data: List[Dict[str, Any]]):
        """Ingest inventory data into ClickHouse"""
        if not self.clickhouse_client:
            logger.error("ClickHouse client not available")
            return

        try:
            clickhouse_data = [
                (
                    record["id"],
                    record["store"],
                    record["product"],
                    record["current_stock"],
                    record["reorder_level"],
                    record["max_stock"],
                    record["last_restocked"],
                    record["supplier"],
                    record["status"],
                    record["created_at"]
                )
                for record in inventory_data
            ]

            self.clickhouse_client.execute(
                """
                INSERT INTO inventory_data 
                (id, store, product, current_stock, reorder_level, max_stock, 
                 last_restocked, supplier, status, created_at)
                VALUES
                """,
                clickhouse_data
            )

            logger.info(
                f"Ingested {len(inventory_data)} inventory records into ClickHouse")

        except Exception as e:
            logger.error(f"Error ingesting inventory data: {e}")

    def run_initial_ingestion(self):
        """Run initial data ingestion"""
        logger.info("Starting initial data ingestion...")

        # Generate data
        sales_data = self.generate_sales_data(90)  # 3 months of data
        customer_data = self.generate_customer_data(200)
        inventory_data = self.generate_inventory_data()

        # Ingest data
        self.ingest_sales_data(sales_data)
        self.ingest_customer_data(customer_data)
        self.ingest_inventory_data(inventory_data)

        logger.info("Initial data ingestion completed")

    def run_daily_ingestion(self):
        """Run daily data ingestion (for continuous data flow)"""
        logger.info("Running daily data ingestion...")

        # Generate today's sales data
        sales_data = self.generate_sales_data(1)
        self.ingest_sales_data(sales_data)

        logger.info("Daily data ingestion completed")


def main():
    """Main function"""
    logger.info("Starting Data Ingestion Service")

    # Wait for services to be ready
    time.sleep(30)

    service = DataIngestionService()

    # Run initial ingestion
    service.run_initial_ingestion()

    # Schedule daily ingestion
    schedule.every().day.at("00:01").do(service.run_daily_ingestion)

    # Keep running for scheduled tasks
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()

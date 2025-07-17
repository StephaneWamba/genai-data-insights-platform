#!/usr/bin/env python3
"""
ClickHouse Data Population Script

This script populates ClickHouse tables with realistic business data for testing.
Generates hundreds of records for sales_data, customer_data, and inventory_data tables.
"""

import clickhouse_connect
import random
from datetime import datetime, timedelta
import logging
from typing import List, Dict, Any
import os

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ClickHouseDataPopulator:
    """Populates ClickHouse with realistic business data"""

    def __init__(self):
        """Initialize ClickHouse connection"""
        self.client = clickhouse_connect.get_client(
            host='localhost',
            port=8123,
            username='default',
            password='changeme',
            database='default'
        )

        # Business data constants
        self.stores = [
            "Paris Central", "Paris North", "Paris South", "Paris East", "Paris West",
            "London Central", "London North", "London South", "London East", "London West",
            "Berlin Central", "Berlin North", "Berlin South", "Berlin East", "Berlin West",
            "Madrid Central", "Madrid North", "Madrid South", "Madrid East", "Madrid West",
            "Rome Central", "Rome North", "Rome South", "Rome East", "Rome West"
        ]

        self.products = [
            "Running Shoes", "Casual Shoes", "Formal Shoes", "Boots", "Sandals",
            "T-Shirts", "Shirts", "Jeans", "Dresses", "Jackets",
            "Watches", "Bags", "Belts", "Sunglasses", "Jewelry",
            "Laptops", "Smartphones", "Tablets", "Headphones", "Cameras",
            "Sofas", "Tables", "Chairs", "Beds", "Lamps"
        ]

        self.categories = [
            "Footwear", "Apparel", "Accessories", "Electronics", "Home & Garden"
        ]

        self.regions = ["Europe", "North America", "Asia",
                        "South America", "Africa", "Australia"]
        self.age_groups = ["18-25", "26-35", "36-45", "46-55", "55+"]
        self.suppliers = [f"Supplier_{i}" for i in range(1, 21)]

    def generate_sales_data(self, days: int = 90, records_per_day: int = 50) -> List[Dict[str, Any]]:
        """Generate realistic sales data"""
        logger.info(
            f"Generating {days * records_per_day} sales records for {days} days")

        sales_data = []
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        for day in range(days):
            current_date = start_date + timedelta(days=day)

            # Generate daily sales with realistic patterns
            base_sales = records_per_day

            # Weekend effect (30% more sales)
            if current_date.weekday() >= 5:  # Saturday/Sunday
                base_sales = int(base_sales * 1.3)

            # Seasonal effect (higher sales in December)
            if current_date.month == 12:
                base_sales = int(base_sales * 1.5)

            # Monthly variation
            if current_date.month in [6, 7, 8]:  # Summer months
                base_sales = int(base_sales * 1.2)

            for _ in range(base_sales):
                store = random.choice(self.stores)
                product = random.choice(self.products)
                category = random.choice(self.categories)

                # Realistic pricing based on category
                if category == "Electronics":
                    base_price = random.uniform(200, 2000)
                elif category == "Footwear":
                    base_price = random.uniform(50, 300)
                elif category == "Apparel":
                    base_price = random.uniform(30, 200)
                elif category == "Accessories":
                    base_price = random.uniform(20, 500)
                else:  # Home & Garden
                    base_price = random.uniform(100, 800)

                quantity = random.randint(1, 10)
                revenue = base_price * quantity
                cost = revenue * random.uniform(0.4, 0.7)  # 40-70% cost margin
                profit = revenue - cost
                region = random.choice(self.regions)

                sales_record = {
                    "date": current_date.date(),
                    "store": store,
                    "product": product,
                    "category": category,
                    "quantity_sold": quantity,
                    "revenue": round(revenue, 2),
                    "cost": round(cost, 2),
                    "profit": round(profit, 2),
                    "region": region
                }
                sales_data.append(sales_record)

        logger.info(f"Generated {len(sales_data)} sales records")
        return sales_data

    def generate_customer_data(self, count: int = 500) -> List[Dict[str, Any]]:
        """Generate realistic customer data"""
        logger.info(f"Generating {count} customer records")

        customer_data = []

        for i in range(count):
            # Generate realistic customer data
            customer_id = f"CUST_{i+1:06d}"
            name = f"Customer {i+1}"
            email = f"customer{i+1}@example.com"
            region = random.choice(self.regions)
            age_group = random.choice(self.age_groups)

            # Realistic purchase patterns
            total_purchases = random.randint(1, 50)
            total_spent = random.uniform(50, 10000)
            last_purchase = datetime.now() - timedelta(days=random.randint(1, 365))
            preferred_store = random.choice(self.stores)
            preferred_category = random.choice(self.categories)

            customer_record = {
                "customer_id": customer_id,
                "name": name,
                "email": email,
                "region": region,
                "age_group": age_group,
                "total_purchases": total_purchases,
                "total_spent": round(total_spent, 2),
                "last_purchase": last_purchase.date(),
                "preferred_store": preferred_store,
                "preferred_category": preferred_category
            }
            customer_data.append(customer_record)

        logger.info(f"Generated {len(customer_data)} customer records")
        return customer_data

    def generate_inventory_data(self, records_per_product: int = 5) -> List[Dict[str, Any]]:
        """Generate realistic inventory data"""
        logger.info(
            f"Generating inventory data for {len(self.products) * records_per_product} product-store combinations")

        inventory_data = []

        for product in self.products:
            for _ in range(records_per_product):
                store = random.choice(self.stores)
                current_stock = random.randint(0, 500)
                reorder_level = random.randint(10, 100)
                max_stock = random.randint(200, 1000)
                last_restocked = datetime.now() - timedelta(days=random.randint(1, 90))
                supplier = random.choice(self.suppliers)

                # Determine status based on stock level
                if current_stock == 0:
                    status = "Out of Stock"
                elif current_stock <= reorder_level:
                    status = "Low Stock"
                else:
                    status = "In Stock"

                inventory_record = {
                    "store": store,
                    "product": product,
                    "current_stock": current_stock,
                    "reorder_level": reorder_level,
                    "max_stock": max_stock,
                    "last_restocked": last_restocked.date(),
                    "supplier": supplier,
                    "status": status
                }
                inventory_data.append(inventory_record)

        logger.info(f"Generated {len(inventory_data)} inventory records")
        return inventory_data

    def clear_existing_data(self):
        """Clear existing data from all tables"""
        logger.info("Clearing existing data from all tables")

        try:
            self.client.command("TRUNCATE TABLE sales_data")
            self.client.command("TRUNCATE TABLE customer_data")
            self.client.command("TRUNCATE TABLE inventory_data")
            logger.info("Successfully cleared all existing data")
        except Exception as e:
            logger.error(f"Error clearing data: {e}")
            raise

    def insert_sales_data(self, sales_data: List[Dict[str, Any]]):
        """Insert sales data into ClickHouse"""
        logger.info(f"Inserting {len(sales_data)} sales records")

        try:
            # Prepare data for batch insert
            data_to_insert = []
            for record in sales_data:
                data_to_insert.append([
                    record["date"],
                    record["store"],
                    record["product"],
                    record["category"],
                    record["quantity_sold"],
                    record["revenue"],
                    record["cost"],
                    record["profit"],
                    record["region"]
                ])

            self.client.insert("sales_data", data_to_insert, column_names=[
                "date", "store", "product", "category", "quantity_sold",
                "revenue", "cost", "profit", "region"
            ])
            logger.info("Successfully inserted sales data")
        except Exception as e:
            logger.error(f"Error inserting sales data: {e}")
            raise

    def insert_customer_data(self, customer_data: List[Dict[str, Any]]):
        """Insert customer data into ClickHouse"""
        logger.info(f"Inserting {len(customer_data)} customer records")

        try:
            # Prepare data for batch insert
            data_to_insert = []
            for record in customer_data:
                data_to_insert.append([
                    record["customer_id"],
                    record["name"],
                    record["email"],
                    record["region"],
                    record["age_group"],
                    record["total_purchases"],
                    record["total_spent"],
                    record["last_purchase"],
                    record["preferred_store"],
                    record["preferred_category"]
                ])

            self.client.insert("customer_data", data_to_insert, column_names=[
                "customer_id", "name", "email", "region", "age_group",
                "total_purchases", "total_spent", "last_purchase",
                "preferred_store", "preferred_category"
            ])
            logger.info("Successfully inserted customer data")
        except Exception as e:
            logger.error(f"Error inserting customer data: {e}")
            raise

    def insert_inventory_data(self, inventory_data: List[Dict[str, Any]]):
        """Insert inventory data into ClickHouse"""
        logger.info(f"Inserting {len(inventory_data)} inventory records")

        try:
            # Prepare data for batch insert
            data_to_insert = []
            for record in inventory_data:
                data_to_insert.append([
                    record["store"],
                    record["product"],
                    record["current_stock"],
                    record["reorder_level"],
                    record["max_stock"],
                    record["last_restocked"],
                    record["supplier"],
                    record["status"]
                ])

            self.client.insert("inventory_data", data_to_insert, column_names=[
                "store", "product", "current_stock", "reorder_level",
                "max_stock", "last_restocked", "supplier", "status"
            ])
            logger.info("Successfully inserted inventory data")
        except Exception as e:
            logger.error(f"Error inserting inventory data: {e}")
            raise

    def populate_all_data(self, clear_existing: bool = True):
        """Populate all tables with realistic data"""
        logger.info("Starting data population process")

        try:
            # Clear existing data if requested
            if clear_existing:
                self.clear_existing_data()

            # Generate data
            sales_data = self.generate_sales_data(
                days=90, records_per_day=50)  # 4,500 sales records
            customer_data = self.generate_customer_data(
                count=500)  # 500 customers
            inventory_data = self.generate_inventory_data(
                records_per_product=5)  # 125 inventory records

            # Insert data
            self.insert_sales_data(sales_data)
            self.insert_customer_data(customer_data)
            self.insert_inventory_data(inventory_data)

            logger.info("Data population completed successfully!")
            logger.info(f"Total records inserted:")
            logger.info(f"  - Sales: {len(sales_data)}")
            logger.info(f"  - Customers: {len(customer_data)}")
            logger.info(f"  - Inventory: {len(inventory_data)}")

        except Exception as e:
            logger.error(f"Error during data population: {e}")
            raise

    def verify_data(self):
        """Verify that data was inserted correctly"""
        logger.info("Verifying inserted data")

        try:
            sales_count = self.client.query(
                "SELECT COUNT(*) FROM sales_data").result_rows[0][0]
            customer_count = self.client.query(
                "SELECT COUNT(*) FROM customer_data").result_rows[0][0]
            inventory_count = self.client.query(
                "SELECT COUNT(*) FROM inventory_data").result_rows[0][0]

            logger.info(f"Verification results:")
            logger.info(f"  - Sales records: {sales_count}")
            logger.info(f"  - Customer records: {customer_count}")
            logger.info(f"  - Inventory records: {inventory_count}")

            return sales_count > 0 and customer_count > 0 and inventory_count > 0

        except Exception as e:
            logger.error(f"Error verifying data: {e}")
            return False


def main():
    """Main function to run the data population script"""
    logger.info("Starting ClickHouse data population script")

    try:
        populator = ClickHouseDataPopulator()

        # Populate all data
        populator.populate_all_data(clear_existing=True)

        # Verify the data
        if populator.verify_data():
            logger.info(
                "✅ Data population and verification completed successfully!")
        else:
            logger.error("❌ Data verification failed!")

    except Exception as e:
        logger.error(f"❌ Data population failed: {e}")
        raise


if __name__ == "__main__":
    main()

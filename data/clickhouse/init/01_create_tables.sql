-- ClickHouse Data Warehouse Schema
-- Optimized for analytical queries and time-series data
-- Sales data table (partitioned by date for performance)
CREATE TABLE IF NOT EXISTS sales_data (
    id UInt32,
    date Date,
    store String,
    product String,
    category String,
    quantity_sold UInt32,
    revenue Decimal(10, 2),
    cost Decimal(10, 2),
    profit Decimal(10, 2),
    region String,
    created_at DateTime DEFAULT now ()
) ENGINE = MergeTree ()
PARTITION BY
    toYYYYMM (date)
ORDER BY
    (date, store, product) SETTINGS index_granularity = 8192;

-- Customer data table
CREATE TABLE IF NOT EXISTS customer_data (
    customer_id String,
    name String,
    email String,
    region String,
    age_group String,
    total_purchases UInt32,
    total_spent Decimal(10, 2),
    last_purchase Date,
    preferred_store String,
    preferred_category String,
    created_at DateTime DEFAULT now ()
) ENGINE = MergeTree ()
ORDER BY
    (customer_id, region) SETTINGS index_granularity = 8192;

-- Inventory data table
CREATE TABLE IF NOT EXISTS inventory_data (
    id UInt32,
    store String,
    product String,
    current_stock UInt32,
    reorder_level UInt32,
    max_stock UInt32,
    last_restocked Date,
    supplier String,
    status String,
    created_at DateTime DEFAULT now ()
) ENGINE = MergeTree ()
ORDER BY
    (store, product) SETTINGS index_granularity = 8192;

-- Store performance metrics (materialized view)
CREATE MATERIALIZED VIEW IF NOT EXISTS store_performance_mv ENGINE = SummingMergeTree ()
PARTITION BY
    toYYYYMM (date)
ORDER BY
    (date, store) AS
SELECT
    date,
    store,
    region,
    sum(quantity_sold) as total_quantity,
    sum(revenue) as total_revenue,
    sum(profit) as total_profit,
    count() as transaction_count
FROM
    sales_data
GROUP BY
    date,
    store,
    region;

-- Product performance metrics (materialized view)
CREATE MATERIALIZED VIEW IF NOT EXISTS product_performance_mv ENGINE = SummingMergeTree ()
PARTITION BY
    toYYYYMM (date)
ORDER BY
    (date, product, category) AS
SELECT
    date,
    product,
    category,
    sum(quantity_sold) as total_quantity,
    sum(revenue) as total_revenue,
    sum(profit) as total_profit,
    count() as transaction_count
FROM
    sales_data
GROUP BY
    date,
    product,
    category;

-- Daily aggregated metrics
CREATE MATERIALIZED VIEW IF NOT EXISTS daily_metrics_mv ENGINE = SummingMergeTree ()
PARTITION BY
    toYYYYMM (date)
ORDER BY
    date AS
SELECT
    date,
    sum(quantity_sold) as total_quantity,
    sum(revenue) as total_revenue,
    sum(profit) as total_profit,
    count() as transaction_count,
    uniq (store) as active_stores,
    uniq (product) as active_products
FROM
    sales_data
GROUP BY
    date;
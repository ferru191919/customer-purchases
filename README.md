*Customer Purchases Pipeline*
End‑to‑end data engineering project that ingests customer master data from an internal SQLite
source and order data from an external REST API, applies professional data quality checks and
transformations in Python, and loads curated analytics tables into a small data warehouse
(SQLite, star‑schema style).


*How to run*
a. Initialize source DB: python init_source_db.py
b. Initialize warehouse DB: python init_target_db.py
c. Run the ETL pipeline: python etl.py


*Business problem*
A retail/e‑commerce team needs a reliable “Customer Purchases” dataset that combines:

- Customer master data (names, country, created date) in an internal SQLite db
- Order data (who bought what, when, and for how much) from external API

The purpose is to load clean data in a dedicated Data Warehouse in order to perform queries (OLAP).


*Architecture overview*
The pipeline is intentionally small but models real practices:

## Source layer
- Customers table in customers_data_source.db (SQLite)
- Orders API (https://fakeapi.net/orders) returning JSON

## Processing layer
Extraction:
- extract_customers(conn) → pandas DataFrame 
- extract_purchases() → API call → pandas DataFrame

Validation (Row‑level validation with explicit rule masks and error codes):
- validate_customers(df) → splits into valid_customers, invalid_customers 
- validate_purchases(df) → splits into valid_purchases, invalid_purchases

Transformation:
- transform_customers(valid_customers) → dim_customer DataFrame 
- transform_purchases(valid_purchases) → fact_order DataFrame

## Warehouse layer (SQLite, retail_dw.db)
One fact table (orders), and two dimension tables (dim_customer & dq_rejected_orders).
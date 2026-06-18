# Design DB schema for loading transformed data
# Star schema with a fact table and two dimensional tables


import sqlite3
import logging

logger = logging.getLogger(__name__)
TARGET_DB = "retail_dw.db"


# Fact Table
def create_fact_order(conn):
    sql = """
    CREATE TABLE IF NOT EXISTS fact_order (
        order_id            INTEGER PRIMARY KEY,
        customer_id         INTEGER NOT NULL,
        order_date          TEXT NOT NULL,
        amount              REAL NOT NULL,
        is_delivered        INTEGER,
        FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id)
    );
    """
    conn.execute(sql)


# Dimensional table
def create_dim_customer(conn):
    sql = """
    CREATE TABLE IF NOT EXISTS dim_customer (
        customer_id     INTEGER PRIMARY KEY,
        first_name      TEXT NOT NULL,
        last_name       TEXT NOT NULL,
        email           TEXT,
        country         TEXT NOT NULL,
        created_at      TEXT NOT NULL
    );
    """
    conn.execute(sql)


# Dimensional table
def create_dq_rejected_orders(conn):
    sql = """
    CREATE TABLE IF NOT EXISTS dq_rejected_orders (
        id                INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id          INTEGER,
        customer_id       INTEGER,
        raw_payload       TEXT NOT NULL,
        validation_errors TEXT NOT NULL,
        rejected_at       TEXT NOT NULL
    );
    """
    conn.execute(sql)


def main():
    with sqlite3.connect(TARGET_DB) as conn:
        create_dim_customer(conn)
        create_fact_order(conn)
        create_dq_rejected_orders(conn)
        conn.commit()


if __name__ == "__main__":
    main()
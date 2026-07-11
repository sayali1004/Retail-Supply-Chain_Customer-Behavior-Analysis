import duckdb
import pandas as pd
import os

con = duckdb.connect("olist_db.duckdb")

csv_to_table = {
    "data/olist_orders_dataset.csv": "orders",
    "data/olist_order_items_dataset.csv": "order_items",
    "data/olist_customers_dataset.csv": "customers",
    "data/olist_products_dataset.csv": "products",
    "data/olist_sellers_dataset.csv": "sellers",
    "data/olist_order_payments_dataset.csv": "order_payments",
    "data/olist_order_reviews_dataset.csv": "order_reviews",
    "data/olist_geolocation_dataset.csv": "geolocation",
    "data/product_category_name_translation.csv": "product_category_translation",
}

for csv_path, table_name in csv_to_table.items():
    if not os.path.exists(csv_path):
        print(f"⚠️  Missing file: {csv_path}")
        continue

    df = pd.read_csv(csv_path)
    con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM df")
    row_count = con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    print(f"✅ Loaded '{table_name}' — {row_count:,} rows")

print("\n--- Tables in database ---")
tables = con.execute("SHOW TABLES").fetchdf()
print(tables)

con.close()

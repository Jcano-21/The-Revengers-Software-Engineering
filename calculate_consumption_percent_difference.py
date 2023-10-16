import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import mysql.connector

# Set up the SQLAlchemy engine
engine = create_engine('mysql+mysqlconnector://root:Th3RevengersTe4m@localhost/Barrios')

# List of category names
categories = [
    'ACY Inserts',
    'Filter Inserts',
    'Food',
    'Food-RS',
    'Food-US',
    'KTO',
    'Pretreat Tanks'
]

# Dictionary to store counts for each category
counts = {}

# Loop through categories
for category in categories:
    # SQL query for the current category
    query = f"""
        SELECT
            a.datedim,
            a.current_ip_owner,
            SUM(CASE WHEN a.category_name IN ('{category}') AND a.current_ip_owner = 'NASA' THEN 1 ELSE 0 END) AS nasa_count,
            SUM(CASE WHEN a.category_name IN ('{category}') AND a.current_ip_owner = 'RSA00' THEN 1 ELSE 0 END) AS rsa00_count,
            COUNT(DISTINCT CASE WHEN a.category_name IN ('{category}') THEN a.id END) AS distinct_id_count_categories,
            COUNT(DISTINCT CASE WHEN a.category_name IN ('{category}') AND a.status = 'discard' THEN a.id END) AS discard_count
        FROM
            inventory_msc a
        WHERE
            (a.current_ip_owner = 'NASA' OR a.current_ip_owner = 'RSA00')
            AND a.category_name = '{category}'
        GROUP BY
            a.datedim, a.current_ip_owner
        ORDER BY
            a.datedim;

    """

    # Fetch the data into a DataFrame
    df = pd.read_sql(query, engine)

    # Store the DataFrame for the current category
    counts[category] = df

# Print the counts for each category
print("Data for each category:")
for category, df in counts.items():
    print(f"\nCategory: {category}")
    print(df)

# Dispose the SQLAlchemy engine
engine.dispose()
 

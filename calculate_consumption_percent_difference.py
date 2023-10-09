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

# Dictionary to store average rates for each category
average_rates = {}

# Loop through categories
for category in categories:
    # SQL query for the current category
    query = f"""
        SELECT
            a.datedim,
            a.quantity_count,
            LAG(a.quantity_count, 1, 0) OVER (ORDER BY a.datedim) AS prev_quantity_count,
            CASE
                WHEN LAG(a.quantity_count, 1, 0) OVER (ORDER BY a.datedim) = 0 THEN NULL
                ELSE (a.quantity_count - LAG(a.quantity_count, 1, 0) OVER (ORDER BY a.datedim)) / LAG(a.quantity_count, 1, 0) OVER (ORDER BY a.datedim)
            END AS daily_consumption_rate
        FROM
            (
                SELECT
                    datedim,
                    COUNT(quantity) AS quantity_count
                FROM
                    inventory_msc
                WHERE
                    category_name = '{category}'
                GROUP BY
                    datedim
            ) a
        ORDER BY
            a.datedim;
    """

    # Fetch the data into a DataFrame
    df = pd.read_sql(query, engine)

    # Filter positive and non-zero consumption rates
    positive_non_zero_rates = df[df['daily_consumption_rate'] >= 0]

    # Calculate the average
    average_rate = np.mean(positive_non_zero_rates['daily_consumption_rate'])

    # Store the average rate for the current category
    average_rates[category] = average_rate

# Print the average consumption rates for each category
print("Average consumption rates for each category:")
for category, rate in average_rates.items():
    print(f"{category}: {rate}")

# Dispose the SQLAlchemy engine
engine.dispose()



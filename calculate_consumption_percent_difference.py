import pandas as pd
import sqlalchemy as sa
import pymysql
from consumables import Consumables  # Import the Consumables class
import json

def createRequest(consumables, data):
    
    print("Starting Request")
    # Set up the SQLAlchemy engine
    username = 'root'
    password = 'Th3RevengersTe4m'
    db_name = 'barrios'
    
    connection_url = f"mysql+pymysql://{username}:{password}@localhost/{db_name}"

    # Create an SQLAlchemy engine
    engine = sa.create_engine(connection_url)

    print("Engine Created!")
        # SQL query for the current category
    if data['category'] == 'Food-US':
        dataCat = '6'
    elif data['category'] == 'Food':
        dataCat = '6'
    elif data['category'] == 'Food-RS':
        dataCat = '7'
    elif data['category'] == 'ACY Inserts':
        dataCat = '4'
    elif data['category'] == 'Filter Inserts':
        dataCat = '5'
    elif data['category'] == 'KTO':
        dataCat = '3'
    elif data['category'] == 'Pretreat Tanks':
        dataCat = '2'

    query_category = f"""
        SELECT
            a.datedim,
            a.current_ip_owner,
            SUM(CASE WHEN a.categoryid IN ('{dataCat}') AND a.current_ip_owner = 'NASA' THEN 1 ELSE 0 END) AS nasa_count,
            SUM(CASE WHEN a.categoryid IN ('{dataCat}') AND a.current_ip_owner = 'RSA00' THEN 1 ELSE 0 END) AS rsa00_count,
            COUNT(DISTINCT CASE WHEN a.categoryid IN ('{dataCat}') THEN a.id END) AS distinct_id_count_categories,
            COUNT(DISTINCT CASE WHEN a.categoryid IN ('{dataCat}') AND a.status = 'discard' THEN a.id END) AS discard_count,
            COUNT(DISTINCT CASE WHEN a.categoryid IN ('{dataCat}') THEN a.id END) - COUNT(DISTINCT CASE WHEN a.categoryid IN ('{dataCat}') AND a.status = 'discard' THEN a.id END) AS distinct_discard_difference
        FROM
            inventory_msc a
        WHERE
            (a.current_ip_owner = 'NASA' OR a.current_ip_owner = 'RSA00')
            AND a.categoryid = '{dataCat}'
            AND a.datedim BETWEEN '{data['start_date']}' AND '{data['end_date']}'
        GROUP BY
            a.datedim, a.current_ip_owner
        ORDER BY
        a.datedim;

        """

 
    # Fetch the data into a DataFrame
    df_category = pd.read_sql(query_category, engine)
    consumables.load_category_data(data['category'], df_category)
    
    print('Here is the data:', data)


    print(f'Requesting crew counts from dates. ')


    rs_consumables, us_consumables, category_info = consumables.get_consumables_for_date_range(data['start_date'], data['end_date'], data['category'])

    # Dispose the SQLAlchemy engine
    engine.dispose()

    df_list = [rs_consumables, us_consumables, category_info]

    # create an empty dictionary
    frames = {}

    # loop through the list of dataframes and assign each to a key
    for i, df in enumerate(df_list):
      frames[f'df{i+1}'] = df

    # print the dictionary of dataframes
    print('Print the dict of dfs: ', frames)


    return(frames)
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


    # Loop through crew types
    for crew_type in ['US', 'RS']:
        # SQL query for the current crew type
        query_crew = f"""
            SELECT
                a.datedim,
                SUM(a.crew_count) AS {crew_type}_crew_count
            FROM
                iss_flight_plan_crew a
            WHERE
                a.crew_type = '{crew_type}'
                AND a.datedim BETWEEN '{data['start_date']}' AND '{data['end_date']}'  -- Include date range condition
            GROUP BY
                a.datedim
            ORDER BY
                a.datedim;
            """

        # Fetch the data into a DataFrame
        df_crew = pd.read_sql(query_crew, engine)
        if crew_type == 'RS':
            consumables.load_RS_crew_count(df_crew)
        elif crew_type == 'US':
            consumables.load_US_crew_count(df_crew)

    # Loop through categories
    #for category in categories:
        # SQL query for the current category
    query_category = f"""
        SELECT
            a.datedim,
            a.current_ip_owner,
            SUM(CASE WHEN a.category_name IN ('{data['category']}') AND a.current_ip_owner = 'NASA' THEN 1 ELSE 0 END) AS nasa_count,
            SUM(CASE WHEN a.category_name IN ('{data['category']}') AND a.current_ip_owner = 'RSA00' THEN 1 ELSE 0 END) AS rsa00_count,
            COUNT(DISTINCT CASE WHEN a.category_name IN ('{data['category']}') THEN a.id END) AS distinct_id_count_categories,
            COUNT(DISTINCT CASE WHEN  a.category_name IN ('{data['category']}') AND a.status = 'discard' THEN a.id END) AS discard_count
        FROM
            inventory_msc a
        WHERE
            (a.current_ip_owner = 'NASA' OR a.current_ip_owner = 'RSA00')
            AND a.category_name = '{data['category']}'
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

    print('Requesting', data['category'], 'from class.')

    category_info = consumables.get_consumables_for_date_range(data['start_date'], data['end_date'], data['category'])
    RS_crew_info, US_crew_info = consumables.get_Ccount_for_date_range(data['start_date'], data['end_date'])

    # Dispose the SQLAlchemy engine
    engine.dispose()

    df_list = [category_info, US_crew_info, RS_crew_info]

    # create an empty dictionary
    frames = {}

    # loop through the list of dataframes and assign each to a key
    for i, df in enumerate(df_list):
      frames[f'df{i+1}'] = df

    # print the dictionary of dataframes
    print('Print the dict of dfs: ', frames)


    return(frames)
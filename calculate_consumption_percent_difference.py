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
                AND a.datedim BETWEEN '{data['start_date']}' AND '{data['end_date']}'
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
            COUNT(DISTINCT CASE WHEN  a.categoryid IN ('{dataCat}') AND a.status = 'discard' THEN a.id END) AS discard_count
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


    category_info = consumables.get_consumables_for_date_range(data['start_date'], data['end_date'], data['category'])

    # Dispose the SQLAlchemy engine
    engine.dispose()

    category_info = category_info.to_json(orient='table')


    return(category_info)
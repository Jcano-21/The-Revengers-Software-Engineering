import pandas as pd
import sqlalchemy as sa
import pymysql
from crews import crews  # Import the Consumables class
import json

def getCrewCounts(crew, data):
    
    print("Starting Request")
    # Set up the SQLAlchemy engine
    username = 'root'
    password = 'Th3RevengersTe4m'
    db_name = 'barrios'
    
    connection_url = f"mysql+pymysql://{username}:{password}@localhost/{db_name}"

    # Create an SQLAlchemy engine
    engine = sa.create_engine(connection_url)

    print("Engine Created!")

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
            crew.load_RS_crew_count(df_crew)
        elif crew_type == 'US':
            crew.load_US_crew_count(df_crew)
    
    print('Here is the data:', data)


    print(f'Requesting crew counts from dates. ')

    print('Requesting', data['category'], 'from class.')

    RS_crew_info, US_crew_info = crew.get_Ccount_for_date_range(data['start_date'], data['end_date'])

    # Dispose the SQLAlchemy engine
    engine.dispose()

    df_list = [US_crew_info, RS_crew_info]

    # create an empty dictionary
    frames = {}

    # loop through the list of dataframes and assign each to a key
    for i, df in enumerate(df_list):
      frames[f'df{i+1}'] = df

    # print the dictionary of dataframes
    print('Print the dict of dfs: ', frames)


    return(frames)
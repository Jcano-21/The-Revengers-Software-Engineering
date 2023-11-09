import pandas as pd
import sqlalchemy as sa
import pymysql
from flights import flights
import json

def getFlights(flights, data):

    print("Starting Request")
    # Set up the SQLAlchemy engine
    username = 'root'
    password = 'Th3RevengersTe4m'
    db_name = 'barrios'
    
    connection_url = f"mysql+pymysql://{username}:{password}@localhost/{db_name}"

    # Create an SQLAlchemy engine
    engine = sa.create_engine(connection_url)

    #THIS CODE NEEDS TO BE MODIFIED TO QUERY BY RESUPPLY VEHICLES DATABASE NEEDS TO BE UPDATED

    #start query
    query_category = f"""
        SELECT
            a.datedim,
            a.vehicle_name
        FROM
            iss_flight_plan a
        WHERE
            a.event = 'Dock'
            AND a.datedim BETWEEN '{data['start_date']}' AND '{data['end_date']}'
        ORDER BY
            a.datedim;
        """

 
    # Fetch the data into a DataFrame
    df_resupply = pd.read_sql(query_category, engine)
    flights.load_flights_data(df_resupply)

    # Dispose the SQLAlchemy engine
    engine.dispose()

    flights_info = flights.get_flights_for_date_range(data['start_date'], data['end_date'])

    flights_info = flights_info.to_json(orient='table')

    return(flights_info)
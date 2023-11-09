import pandas as pd
import sqlalchemy as sa
import pymysql
from waterAndGases import waterAndGases
import json

def getWaterAndGas(waterAndGas, data):

    print("Starting Request")
    # Set up the SQLAlchemy engine
    username = 'root'
    password = 'Th3RevengersTe4m'
    db_name = 'barrios'
    
    connection_url = f"mysql+pymysql://{username}:{password}@localhost/{db_name}"

    # Create an SQLAlchemy engine
    engine = sa.create_engine(connection_url)

    #THIS CODE NEEDS TO BE MODIFIED TO QUERY BY RESUPPLY VEHICLES DATABASE NEEDS TO BE UPDATED
    print('You made it to the water and gas query.')
    if data['category'] == 'US-Water':
        table = 'us_weekly_consumable_water'
        print('You chose US')
        print('Tabe: ', table)
    elif data['category'] == 'RS-Water':
        table = 'rsa_consumable_water'
        print('You chose RS')
        print('Tabe: ', table)
    elif data['category'] == 'Gases':
        table = 'us_rs_weekly_consumable_gas'
        print('You chose GAS')
        print('Tabe: ', table)
    #start query
    query_category = f"""
        SELECT
            *
        FROM
            {table}
        WHERE
             datedim BETWEEN '{data['start_date']}' AND '{data['end_date']}'
        ORDER BY
            datedim;
        """

 
    # Fetch the data into a DataFrame
    df_resupply = pd.read_sql(query_category, engine)
    print('Here is the dataframe of waterAndGas: ', df_resupply)

    if data['category'] == 'US-Water':
        waterAndGas.load_USWater_data(df_resupply)
        print('Data Loaded!')

    elif data['category'] == 'RS-Water':
        waterAndGas.load_RSWater_data(df_resupply)

    elif data['category'] == 'Gases':
        waterAndGas.load_Gas_data(df_resupply)

    # Dispose the SQLAlchemy engine
    engine.dispose()

    if data['category'] == 'US-Water':
        print('retrieve dates: ')
        waterAndGas_info = waterAndGas.get_USWater_for_date_range(data['start_date'], data['end_date'])

    elif data['category'] == 'RS-Water':
        waterAndGas_info = waterAndGas.get_RSWater_for_date_range(data['start_date'], data['end_date'])

    elif data['category'] == 'Gases':
        waterAndGas_info = waterAndGas.get_Gas_for_date_range(data['start_date'], data['end_date'])

    waterAndGas_info = waterAndGas_info.to_json(orient='table')

    return(waterAndGas_info)
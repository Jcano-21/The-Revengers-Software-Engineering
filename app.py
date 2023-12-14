from flask import Flask, render_template, request, jsonify
from consumables import Consumables
import pandas as pd
import numpy as np
import json as js
from consumables_query import createRequest
from consumables_query import get_resupply_dates
from flights_query import getFlights
from flights import flights
from waterAndGases import waterAndGases
from waterAndGases_query import getWaterAndGas
from crews import crews
from crews_query import getCrewCounts
import sqlalchemy as sa
import pymysql
from modal import request_modal_update
from modal import request_modal_update_RSWater
from modal import request_modal_update_USWater
from modal import request_modal_update_Gas

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/index.html")
def index_call():
    return render_template("index.html")


@app.route("/info.html")
def info():
    return render_template("info.html")


@app.route("/consumable", methods=['POST'])
def consumable():
    data = request.get_json()  # Extract JSON data from the request

    flight = flights()
    flights_data = getFlights(flight, data)

    crew = crews()
    crew_data = getCrewCounts(crew, data)

    UScrew_counts_data = crew_data['df1']
    RScrew_counts_data = crew_data['df2']
    UScrew_counts_json = UScrew_counts_data.to_json(orient='table')
    RScrew_counts_json = RScrew_counts_data.to_json(orient='table')

    if data['category'] != 'RS-Water' and data['category'] != 'US-Water' and data['category'] != 'Gases':

        # Create an instance of the Consumables class
        consumables = Consumables(data['category'])
        results = createRequest(consumables, data)
        rs_consumables = results['df1']
        us_consumables = results['df2']
        category_info = results['df3']
        rs_consumables_json = rs_consumables.to_json(orient='table')
        us_consumables_json = us_consumables.to_json(orient='table')
        consumables_json = category_info.to_json(orient='table')

        if (data['category'] != 'Food'):
            consumption = consumables.calculate_something(
                data['start_date'], data['end_date'], data['category'], crew_data)

        # print('PRINTING flights_data FROM APP.PY REQUEST:', flights_data)

        # List to make keys for dictionary
        if (data['category'] != 'Food'):
            df_list = [consumables_json, UScrew_counts_json, RScrew_counts_json,
                       flights_data, consumption, rs_consumables_json, us_consumables_json]
        else:
            df_list = [consumables_json, UScrew_counts_json,
                       RScrew_counts_json, flights_data]

        frames = {}

        for i, Any in enumerate(df_list):
            frames[f'df{i+1}'] = Any
            newDataJson = js.dumps(frames)

        # print('Json string of data: ', newDataJson)

        return jsonify(newDataJson)
    else:
        waterAndGas = waterAndGases(data['category'])
        results = getWaterAndGas(waterAndGas, data)
        print('You selected water or Gas.', results)

        if data['category'] == 'US-Water':
            waterConsumption = waterAndGas.calculate_US_water(
                data['start_date'], data['end_date'])

            df_list = [results, UScrew_counts_json,
                       RScrew_counts_json, flights_data, waterConsumption]
        elif data['category'] == 'RS-Water':
            waterConsumption = waterAndGas.calculate_RS_water(
                data['start_date'], data['end_date'])

            df_list = [results, UScrew_counts_json,
                       RScrew_counts_json, flights_data, waterConsumption]

        else:
            df_list = [results, UScrew_counts_json,
                       RScrew_counts_json, flights_data]

        frames = {}

        for i, Any in enumerate(df_list):
            frames[f'df{i+1}'] = Any
            newDataJson = js.dumps(frames)

        return jsonify(newDataJson)


@app.route("/consumptionRates", methods=['POST'])
def consumptionRates():
    category_data = request.get_json()  # Extract JSON data from the request

    # flight = flights()
    # flights_data = getFlights(flight, data)
    start_date = '2022-01-01'
    end_date = '2023-09-05'
    category = category_data

    data = {}

    data[f'start_date'] = start_date
    data[f'end_date'] = end_date
    data[f'category'] = category
    print(data)

    if data['category'] != 'RS-Water' and data['category'] != 'US-Water' and data['category'] != 'Gases':
        flight = flights()
        flights_data = getFlights(flight, data)
        flightPlan = flight.get_flight_data()
        # Create an instance of the Consumables class
        consumables = Consumables(data['category'])
        consumables.load_flights_data(flightPlan)
        createRequest(consumables, data)
        get_resupply_dates(consumables, data)

        trashOne, trashTwo, countData = consumables.get_consumables_for_date_range(
            data['start_date'], data['end_date'], data['category'])

        resupply_dates = consumables.find_resupply_dates(countData)
        results, periods = consumables.calulateResupply(resupply_dates)
        resupply = consumables.get_resupply_dates()
        newDataJson = resupply.to_json()
        print('periods: ', periods)
        print('Resupply: ', resupply)
        print('found dates: ', resupply_dates)

    elif data['category'] == 'RS-Water':
        flight = flights()
        flights_data = getFlights(flight, data)
        flightPlan = flight.get_flight_data()
        # Create an instance of the waterAndGases class
        WandG = waterAndGases(data['category'])
        WandG.load_flights_data(flightPlan)
        getWaterAndGas(WandG, data)

        countData = WandG.get_RSWater_for_date_range(
            data['start_date'], data['end_date'])

        resupply_dates = WandG.find_resupply_datesRS(countData)
        results, periods = WandG.calulateResupplyRS(resupply_dates)
        df = pd.DataFrame(resupply_dates)
        newDataJson = df.to_json()
        print('periods: ', periods)
        print('Resupply: ', newDataJson)
        print('results: ', results)
        print(flightPlan)

    elif data['category'] == 'US-Water':
        flight = flights()
        flights_data = getFlights(flight, data)
        flightPlan = flight.get_flight_data()
        # Create an instance of the waterAndGases class
        WandG = waterAndGases(data['category'])
        WandG.load_flights_data(flightPlan)
        getWaterAndGas(WandG, data)

        countData = WandG.get_USWater_for_date_range(
            data['start_date'], data['end_date'])

        resupply_dates = WandG.find_resupply_datesUS(countData)
        results, periods = WandG.calulateResupplyUS(resupply_dates)
        df = pd.DataFrame(resupply_dates)
        newDataJson = df.to_json()
        print('periods: ', periods)
        print('Resupply: ', newDataJson)
        print('results: ', results)
        print(flightPlan)

    elif data['category'] == 'Gases':
        flight = flights()
        flights_data = getFlights(flight, data)
        flightPlan = flight.get_flight_data()
        # Create an instance of the waterAndGases class
        WandG = waterAndGases(data['category'])
        WandG.load_flights_data(flightPlan)
        getWaterAndGas(WandG, data)

        countData = WandG.get_Gas_for_date_range(
            data['start_date'], data['end_date'])

        resupply_dates = WandG.find_resupply_datesGAS(countData)
        results, periods = WandG.calulateResupplyGas(resupply_dates)
        df = pd.DataFrame(resupply_dates)
        newDataJson = df.to_json()
        print('periods: ', periods)
        print('Resupply: ', newDataJson)
        print('results: ', results)
        print(flightPlan)
    return jsonify(results, periods, newDataJson)


@app.route("/makePredictions", methods=['POST'])
def makePredictions():

    data = request.get_json()  # Extract JSON data from the request

    if data == 'Inventory':
        start_date = '2022-01-01'
        end_date = '2023-09-05'

        categoryOne = 'ACY Inserts'
        categoryTwo = 'Filter Inserts'
        categoryThree = 'Food-RS'
        categoryFour = 'Food-US'
        categoryFive = 'KTO'
        categorySix = 'Pretreat Tanks'

        dataOne = {}
        dataTwo = {}
        dataThree = {}
        dataFour = {}
        dataFive = {}
        dataSix = {}

        dataOne[f'start_date'] = start_date
        dataOne[f'end_date'] = end_date
        dataOne[f'category'] = categoryOne

        dataTwo[f'start_date'] = start_date
        dataTwo[f'end_date'] = end_date
        dataTwo[f'category'] = categoryTwo

        dataThree[f'start_date'] = start_date
        dataThree[f'end_date'] = end_date
        dataThree[f'category'] = categoryThree

        dataFour[f'start_date'] = start_date
        dataFour[f'end_date'] = end_date
        dataFour[f'category'] = categoryFour

        dataFive[f'start_date'] = start_date
        dataFive[f'end_date'] = end_date
        dataFive[f'category'] = categoryFive

        dataSix[f'start_date'] = start_date
        dataSix[f'end_date'] = end_date
        dataSix[f'category'] = categorySix

        ACY = Consumables(categoryOne)
        FilterInserts = Consumables(categoryTwo)
        FoodRS = Consumables(categoryThree)
        FoodUS = Consumables(categoryFour)
        KTO = Consumables(categoryFive)
        PretreatTanks = Consumables(categorySix)

        createRequest(ACY, dataOne)
        createRequest(FilterInserts, dataTwo)
        createRequest(FoodRS, dataThree)
        createRequest(FoodUS, dataFour)
        createRequest(KTO, dataFive)
        createRequest(PretreatTanks, dataSix)

        flight = flights()
        flights_data = getFlights(flight, dataOne)
        flightPlan = flight.get_flight_data()
        # Create an instance of the Consumables class
        ACY.load_flights_data(flightPlan)
        FilterInserts.load_flights_data(flightPlan)
        FoodRS.load_flights_data(flightPlan)
        FoodUS.load_flights_data(flightPlan)
        KTO.load_flights_data(flightPlan)
        PretreatTanks.load_flights_data(flightPlan)

        get_resupply_dates(ACY, dataOne)
        get_resupply_dates(FilterInserts, dataTwo)
        get_resupply_dates(FoodRS, dataThree)
        get_resupply_dates(FoodUS, dataFour)
        get_resupply_dates(KTO, dataFive)
        get_resupply_dates(PretreatTanks, dataSix)


        

        rsOne, usOne, dfOne = ACY.get_consumables_for_date_range(
            dataOne['start_date'], dataOne['end_date'], dataOne['category'])
        rsTwo, usTwo, dfTwo = FilterInserts.get_consumables_for_date_range(
            dataTwo['start_date'], dataTwo['end_date'], dataTwo['category'])
        rsThree, usThree, dfThree = FoodRS.get_consumables_for_date_range(
            dataThree['start_date'], dataThree['end_date'], dataThree['category'])
        rsFour, usFour, dfFour = FoodUS.get_consumables_for_date_range(
            dataFour['start_date'], dataFour['end_date'], dataFour['category'])
        rsFive, usFive, dfFive = KTO.get_consumables_for_date_range(
            dataFive['start_date'], dataFive['end_date'], dataFive['category'])
        rsSix, usSix, dfSix = PretreatTanks.get_consumables_for_date_range(
            dataSix['start_date'], dataSix['end_date'], dataSix['category'])
        
        dataACY = ACY.get_category_data()
        resupply_dates = ACY.find_resupply_dates(dfOne)
        resupplyOne, periods = ACY.calulateResupply(resupply_dates)

        dataFilterInserts = FilterInserts.get_category_data()
        resupply_dates = FilterInserts.find_resupply_dates(dfTwo)
        resupplyTwo, periods = FilterInserts.calulateResupply(resupply_dates)

        dataFoodRS = FoodRS.get_category_data()
        resupply_dates = FoodRS.find_resupply_dates(dfThree)
        resupplyThree, periods = FoodRS.calulateResupply(resupply_dates)

        dataFoodUS = FoodUS.get_category_data()
        resupply_dates = FoodUS.find_resupply_dates(dfFour)
        resupplyFour, periods = FoodUS.calulateResupply(resupply_dates)

        dataKTO = KTO.get_category_data()
        resupply_dates = KTO.find_resupply_dates(dfFive)
        resupplyFive, periods = KTO.calulateResupply(resupply_dates)

        dataPretreatTanks = PretreatTanks.get_category_data()
        resupply_dates = PretreatTanks.find_resupply_dates(dfSix)
        resupplySix, periods = PretreatTanks.calulateResupply(resupply_dates)

        dfOneCalc = ACY.get_resupply_data()
        dfTwoCalc = FilterInserts.get_resupply_data()
        dfThreeCalc = FoodRS.get_resupply_data()
        dfFourCalc = FoodUS.get_resupply_data()
        dfFiveCalc = KTO.get_resupply_data()
        dfSixCalc = PretreatTanks.get_resupply_data()
        df_resupply_quantities = pd.concat(
            [dfOneCalc, dfTwoCalc, dfThreeCalc, dfFourCalc, dfFiveCalc, dfSixCalc], ignore_index=True)

        print('Resupply ACY: ', resupplyOne)
        print('Resupply Filter Inserts: ', resupplyTwo)
        print('Resupply Food-RS: ', resupplyThree)
        print('Resupply Food-US: ', resupplyFour)
        print('Resupply KTO: ', resupplyFive)
        print('Resupply Pretreat Tanks: ', resupplySix)

        dfOne['Category'] = categoryOne
        dfTwo['Category'] = categoryTwo
        dfThree['Category'] = categoryThree
        dfFour['Category'] = categoryFour
        dfFive['Category'] = categoryFive
        dfSix['Category'] = categorySix

        df_Inventory = pd.concat(
            [dfOne, dfTwo, dfThree, dfFour, dfFive, dfSix], ignore_index=True)

        print(df_Inventory)

        start_date = '2022-01-01'
        end_date_Flights = '2025-12-22'

        categoryFlights = 'ACY Inserts'

        dataFlights = {}

        dataFlights[f'start_date'] = start_date
        dataFlights[f'end_date'] = end_date_Flights
        dataFlights[f'category'] = categoryFlights

        flight = flights()
        getFlights(flight, dataFlights)
        df_flight_plan = flight.get_flights_for_date_range(
        dataFlights['start_date'], dataFlights['end_date'])

        model = request_modal_update(
            df_Inventory, df_flight_plan, df_resupply_quantities)
        # request_modal_LR_update(df_Inventory, df_flight_plan, df_resupply_quantities)
        print(df_resupply_quantities)
        print('Model: ', model)
        model_json = model.to_json(orient='table')
        # resupplyOne_json = resupplyOne.to_json(orient='table')
        # resupplyTwo_json = resupplyTwo.to_json(orient='table')
        # resupplyThree_json = resupplyThree.to_json(orient='table')
        # resupplyFour_json = resupplyFour.to_json(orient='table')
        # resupplyFive_json = resupplyFive.to_json(orient='table')
        # resupplySix_json = resupplySix.to_json(orient='table')


        print('predictions json: ', model_json)
        return jsonify(model_json, resupplyOne, resupplyTwo, resupplyThree, resupplyFour, resupplyFive, resupplySix)

    
    elif data == 'RS-Water':
        
        start_date = '2022-01-01'
        end_date = '2023-09-05'

        categoryOne = 'RS-Water'
        categoryTwo = 'US-Water'
        categoryThree = 'Gases'
        

        dataOne = {}
        dataTwo = {}
        dataThree = {}


        dataOne[f'start_date'] = start_date
        dataOne[f'end_date'] = end_date
        dataOne[f'category'] = categoryOne

        dataTwo[f'start_date'] = start_date
        dataTwo[f'end_date'] = end_date
        dataTwo[f'category'] = categoryTwo

        dataThree[f'start_date'] = start_date
        dataThree[f'end_date'] = end_date
        dataThree[f'category'] = categoryThree

        
        RSWater = waterAndGases(categoryOne)
        USWater = waterAndGases(categoryTwo)
        Gases = waterAndGases(categoryThree)
        
        getWaterAndGas(RSWater, dataOne)
        getWaterAndGas(USWater, dataTwo)
        getWaterAndGas(Gases, dataThree)
        
        flight = flights()
        flights_data = getFlights(flight, dataOne)
        flightPlan = flight.get_flight_data()
        # Create an instance of the Consumables class
        RSWater.load_flights_data(flightPlan)
        USWater.load_flights_data(flightPlan)
        Gases.load_flights_data(flightPlan)
        
        get_resupply_dates(RSWater, dataOne)
        get_resupply_dates(USWater, dataTwo)
        get_resupply_dates(Gases, dataThree)
        
        dataRSWater = RSWater.get_rswater_data()
        resupply_dates = RSWater.find_resupply_datesRS(dataRSWater)
        resupplyOne, periods = RSWater.calulateResupplyRS(resupply_dates)

        dataUSWater = USWater.get_uswater_data()
        resupply_dates = USWater.find_resupply_datesUS(dataUSWater)
        resupplyTwo, periods = USWater.calulateResupplyUS(resupply_dates)

        dataGases = Gases.get_gases_data()
        resupply_dates = Gases.find_resupply_datesGAS(dataGases)
        resupplyThree, periods = Gases.calulateResupplyGas(resupply_dates)

        print('Resupply RSWater: ', resupplyOne)
        print('Resupply USWater: ', resupplyTwo)
        print('Resupply Gases: ', resupplyThree)
  

        dfOne = RSWater.get_resupply_data()
        dfTwo = USWater.get_resupply_data()
        dfThree = Gases.get_resupply_data()
        resupply = dfOne
        df_resupply_quantities = pd.concat(
            [dfOne, dfTwo, dfThree], ignore_index=True)

        dfOne = RSWater.get_RSWater_for_date_range(
            dataOne['start_date'], dataOne['end_date'])
        dfTwo = USWater.get_USWater_for_date_range(
            dataTwo['start_date'], dataTwo['end_date'])
        dfThree = Gases.get_Gas_for_date_range(
            dataThree['start_date'], dataThree['end_date'])
       
        dfOne['Category'] = categoryOne
        dfTwo['Category'] = categoryTwo
        dfThree['Category'] = categoryThree
        
        # Assuming 'datedim' is your common column
        # Assuming 'datedim' is your common column
        all_dates = pd.concat([dfOne['datedim'], dfTwo['datedim'], dfThree['datedim']]).unique()

        # Create empty dataframe with all_dates
        df_combined = pd.DataFrame({'datedim': all_dates})

        # Merge dataframes using outer join
        df_combined = pd.merge(df_combined, dfOne, on='datedim', how='outer', suffixes=('', '_dfOne'))
        df_combined = pd.merge(df_combined, dfTwo, on='datedim', how='outer', suffixes=('', '_dfTwo'))
        df_combined = pd.merge(df_combined, dfThree, on='datedim', how='outer', suffixes=('', '_dfThree'))

        # Fill NaN values with 0
        df_combined = df_combined.fillna(0)

        print('Combined DataFrame:')
        print(df_combined)
        print('df 1: ', dfOne, 'df 2 : ', dfTwo, 'df 3: ', dfThree)
        print('Dataframe water and gases: ', df_combined)

        start_date = '2022-01-01'
        end_date_Flights = '2025-12-22'

        categoryFlights = 'ACY Inserts'

        dataFlights = {}

        dataFlights[f'start_date'] = start_date
        dataFlights[f'end_date'] = end_date_Flights
        dataFlights[f'category'] = categoryFlights

        flight = flights()
        getFlights(flight, dataFlights)
        df_flight_plan = flight.get_flights_for_date_range(
            dataFlights['start_date'], dataFlights['end_date'])

        model = request_modal_update_RSWater(
            dfOne, df_flight_plan, resupply)
        # request_modal_LR_update(df_Inventory, df_flight_plan, df_resupply_quantities)
        print(df_resupply_quantities)
        print('Model: ', model)
        model_json = model.to_json(orient='table')
        #print('predictions json: ', model_json)
        return jsonify(model_json)


    elif data == 'US-Water':
        
        start_date = '2022-01-01'
        end_date = '2023-09-05'

        categoryOne = 'RS-Water'
        categoryTwo = 'US-Water'
        categoryThree = 'Gases'
        

        dataOne = {}
        dataTwo = {}
        dataThree = {}


        dataOne[f'start_date'] = start_date
        dataOne[f'end_date'] = end_date
        dataOne[f'category'] = categoryOne

        dataTwo[f'start_date'] = start_date
        dataTwo[f'end_date'] = end_date
        dataTwo[f'category'] = categoryTwo

        dataThree[f'start_date'] = start_date
        dataThree[f'end_date'] = end_date
        dataThree[f'category'] = categoryThree

        
        RSWater = waterAndGases(categoryOne)
        USWater = waterAndGases(categoryTwo)
        Gases = waterAndGases(categoryThree)
        
        getWaterAndGas(RSWater, dataOne)
        getWaterAndGas(USWater, dataTwo)
        getWaterAndGas(Gases, dataThree)
        
        flight = flights()
        flights_data = getFlights(flight, dataOne)
        flightPlan = flight.get_flight_data()
        # Create an instance of the Consumables class
        RSWater.load_flights_data(flightPlan)
        USWater.load_flights_data(flightPlan)
        Gases.load_flights_data(flightPlan)
        
        get_resupply_dates(RSWater, dataOne)
        get_resupply_dates(USWater, dataTwo)
        get_resupply_dates(Gases, dataThree)
        
        dataRSWater = RSWater.get_rswater_data()
        resupply_dates = RSWater.find_resupply_datesRS(dataRSWater)
        resupplyOne, periods = RSWater.calulateResupplyRS(resupply_dates)

        dataUSWater = USWater.get_uswater_data()
        resupply_dates = USWater.find_resupply_datesUS(dataUSWater)
        resupplyTwo, periods = USWater.calulateResupplyUS(resupply_dates)

        dataGases = Gases.get_gases_data()
        resupply_dates = Gases.find_resupply_datesGAS(dataGases)
        resupplyThree, periods = Gases.calulateResupplyGas(resupply_dates)

        print('Resupply RSWater: ', resupplyOne)
        print('Resupply USWater: ', resupplyTwo)
        print('Resupply Gases: ', resupplyThree)
  

        dfOne = RSWater.get_resupply_data()
        dfTwo = USWater.get_resupply_data()
        dfThree = Gases.get_resupply_data()
        resupply = dfTwo        
        df_resupply_quantities = pd.concat(
            [dfOne, dfTwo, dfThree], ignore_index=True)

        dfOne = RSWater.get_RSWater_for_date_range(
            dataOne['start_date'], dataOne['end_date'])
        dfTwo = USWater.get_USWater_for_date_range(
            dataTwo['start_date'], dataTwo['end_date'])
        dfThree = Gases.get_Gas_for_date_range(
            dataThree['start_date'], dataThree['end_date'])
       
        dfOne['Category'] = categoryOne
        dfTwo['Category'] = categoryTwo
        dfThree['Category'] = categoryThree
        
        # Assuming 'datedim' is your common column
        # Assuming 'datedim' is your common column
        all_dates = pd.concat([dfOne['datedim'], dfTwo['datedim'], dfThree['datedim']]).unique()

        # Create empty dataframe with all_dates
        df_combined = pd.DataFrame({'datedim': all_dates})

        # Merge dataframes using outer join
        df_combined = pd.merge(df_combined, dfOne, on='datedim', how='outer', suffixes=('', '_dfOne'))
        df_combined = pd.merge(df_combined, dfTwo, on='datedim', how='outer', suffixes=('', '_dfTwo'))
        df_combined = pd.merge(df_combined, dfThree, on='datedim', how='outer', suffixes=('', '_dfThree'))

        # Fill NaN values with 0
        df_combined = df_combined.fillna(0)

        print('Combined DataFrame:')
        print(df_combined)
        print('df 1: ', dfOne, 'df 2 : ', dfTwo, 'df 3: ', dfThree)
        print('Dataframe water and gases: ', df_combined)

        start_date = '2022-01-01'
        end_date_Flights = '2025-12-22'

        categoryFlights = 'ACY Inserts'

        dataFlights = {}

        dataFlights[f'start_date'] = start_date
        dataFlights[f'end_date'] = end_date_Flights
        dataFlights[f'category'] = categoryFlights

        flight = flights()
        getFlights(flight, dataFlights)
        df_flight_plan = flight.get_flights_for_date_range(
            dataFlights['start_date'], dataFlights['end_date'])

        model = request_modal_update_USWater(
            dfTwo, df_flight_plan, resupply)
        # request_modal_LR_update(df_Inventory, df_flight_plan, df_resupply_quantities)
        print(df_resupply_quantities)
        print('Model: ', model)
        model_json = model.to_json(orient='table')
        #print('predictions json: ', model_json)
        return jsonify(model_json)


    elif data == 'Gases':
        
        start_date = '2022-01-01'
        end_date = '2023-09-05'

        categoryOne = 'RS-Water'
        categoryTwo = 'US-Water'
        categoryThree = 'Gases'
        

        dataOne = {}
        dataTwo = {}
        dataThree = {}


        dataOne[f'start_date'] = start_date
        dataOne[f'end_date'] = end_date
        dataOne[f'category'] = categoryOne

        dataTwo[f'start_date'] = start_date
        dataTwo[f'end_date'] = end_date
        dataTwo[f'category'] = categoryTwo

        dataThree[f'start_date'] = start_date
        dataThree[f'end_date'] = end_date
        dataThree[f'category'] = categoryThree

        
        RSWater = waterAndGases(categoryOne)
        USWater = waterAndGases(categoryTwo)
        Gases = waterAndGases(categoryThree)
        
        getWaterAndGas(RSWater, dataOne)
        getWaterAndGas(USWater, dataTwo)
        getWaterAndGas(Gases, dataThree)
        
        flight = flights()
        flights_data = getFlights(flight, dataOne)
        flightPlan = flight.get_flight_data()
        # Create an instance of the Consumables class
        RSWater.load_flights_data(flightPlan)
        USWater.load_flights_data(flightPlan)
        Gases.load_flights_data(flightPlan)
        
        get_resupply_dates(RSWater, dataOne)
        get_resupply_dates(USWater, dataTwo)
        get_resupply_dates(Gases, dataThree)
        
        dataRSWater = RSWater.get_rswater_data()
        resupply_dates = RSWater.find_resupply_datesRS(dataRSWater)
        resupplyOne, periods = RSWater.calulateResupplyRS(resupply_dates)

        dataUSWater = USWater.get_uswater_data()
        resupply_dates = USWater.find_resupply_datesUS(dataUSWater)
        resupplyTwo, periods = USWater.calulateResupplyUS(resupply_dates)

        dataGases = Gases.get_gases_data()
        resupply_dates = Gases.find_resupply_datesGAS(dataGases)
        resupplyThree, periods = Gases.calulateResupplyGas(resupply_dates)

        print('Resupply RSWater: ', resupplyOne)
        print('Resupply USWater: ', resupplyTwo)
        print('Resupply Gases: ', resupplyThree)
  

        dfOne = RSWater.get_resupply_data()
        dfTwo = USWater.get_resupply_data()
        dfThree = Gases.get_resupply_data()
        resupply = dfThree        
        df_resupply_quantities = pd.concat(
            [dfOne, dfTwo, dfThree], ignore_index=True)

        dfOne = RSWater.get_RSWater_for_date_range(
            dataOne['start_date'], dataOne['end_date'])
        dfTwo = USWater.get_USWater_for_date_range(
            dataTwo['start_date'], dataTwo['end_date'])
        dfThree = Gases.get_Gas_for_date_range(
            dataThree['start_date'], dataThree['end_date'])
       
        dfOne['Category'] = categoryOne
        dfTwo['Category'] = categoryTwo
        dfThree['Category'] = categoryThree
        
        # Assuming 'datedim' is your common column
        # Assuming 'datedim' is your common column
        all_dates = pd.concat([dfOne['datedim'], dfTwo['datedim'], dfThree['datedim']]).unique()

        # Create empty dataframe with all_dates
        df_combined = pd.DataFrame({'datedim': all_dates})

        # Merge dataframes using outer join
        df_combined = pd.merge(df_combined, dfOne, on='datedim', how='outer', suffixes=('', '_dfOne'))
        df_combined = pd.merge(df_combined, dfTwo, on='datedim', how='outer', suffixes=('', '_dfTwo'))
        df_combined = pd.merge(df_combined, dfThree, on='datedim', how='outer', suffixes=('', '_dfThree'))

        # Fill NaN values with 0
        df_combined = df_combined.fillna(0)

        print('Combined DataFrame:')
        print(df_combined)
        print('df 1: ', dfOne, 'df 2 : ', dfTwo, 'df 3: ', dfThree)
        print('Dataframe water and gases: ', df_combined)

        start_date = '2022-01-01'
        end_date_Flights = '2025-12-22'

        categoryFlights = 'ACY Inserts'

        dataFlights = {}

        dataFlights[f'start_date'] = start_date
        dataFlights[f'end_date'] = end_date_Flights
        dataFlights[f'category'] = categoryFlights

        flight = flights()
        getFlights(flight, dataFlights)
        df_flight_plan = flight.get_flights_for_date_range(
            dataFlights['start_date'], dataFlights['end_date'])

        model = request_modal_update_Gas(
            dfThree, df_flight_plan, resupply)
        # request_modal_LR_update(df_Inventory, df_flight_plan, df_resupply_quantities)
        print(df_resupply_quantities)
        print('Model: ', model)
        model_json = model.to_json(orient='table')
        #print('predictions json: ', model_json)
        return jsonify(model_json)

    





if __name__ == "__main__":
    app.run(debug=True)

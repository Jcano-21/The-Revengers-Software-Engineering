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
            consumption = consumables.calculate_something(data['start_date'], data['end_date'], data['category'], crew_data)

        #print('PRINTING flights_data FROM APP.PY REQUEST:', flights_data)


        #List to make keys for dictionary
        if (data['category'] != 'Food'):
            df_list = [consumables_json, UScrew_counts_json, RScrew_counts_json, flights_data, consumption, rs_consumables_json, us_consumables_json]
        else:
            df_list = [consumables_json, UScrew_counts_json, RScrew_counts_json, flights_data]

        frames = {}

        for i, Any in enumerate(df_list):
            frames[f'df{i+1}'] = Any
            newDataJson = js.dumps(frames)

        #print('Json string of data: ', newDataJson)

        return jsonify(newDataJson)
    else:
        waterAndGas = waterAndGases()
        results = getWaterAndGas(waterAndGas, data)
        print('You selected water or Gas.', results)

        
        if data['category'] == 'US-Water':
            waterConsumption = waterAndGas.calculate_US_water(data['start_date'], data['end_date'])

            df_list = [results, UScrew_counts_json, RScrew_counts_json, flights_data, waterConsumption]
        elif data['category'] == 'RS-Water':
            waterConsumption = waterAndGas.calculate_RS_water(data['start_date'], data['end_date'])

            df_list = [results, UScrew_counts_json, RScrew_counts_json, flights_data, waterConsumption]       
            
        else:
            df_list = [results, UScrew_counts_json, RScrew_counts_json, flights_data]
        
        frames = {}

        for i, Any in enumerate(df_list):
            frames[f'df{i+1}'] = Any
            newDataJson = js.dumps(frames)

        return jsonify(newDataJson)

@app.route("/consumptionRates")
def consumptionRates():
    #request.get_json()  # Extract JSON data from the request

    #flight = flights()
    #flights_data = getFlights(flight, data)
    start_date = '2022-01-01'
    end_date = '2023-09-05'
    category = 'KTO'
        
    data = {}

        
    data[f'start_date'] = start_date
    data[f'end_date'] = end_date
    data[f'category'] = category
    print(data)
        
    
    
    if data['category'] != 'RS-Water' and data['category'] != 'US-Water' and data['category'] != 'Gases':
        
        # Create an instance of the Consumables class
        consumables = Consumables(data['category'])
        createRequest(consumables, data)
        get_resupply_dates(consumables, data)
        results = consumables.calulateResupply()
        return jsonify(results)
    

@app.route("/makePredictions")
def makePredictions():
    
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

    get_resupply_dates(ACY, dataOne)
    get_resupply_dates(FilterInserts, dataTwo)
    get_resupply_dates(FoodRS, dataThree)
    get_resupply_dates(FoodUS, dataFour)
    get_resupply_dates(KTO, dataFive)
    get_resupply_dates(PretreatTanks, dataSix)

    resupplyOne = ACY.calulateResupply()
    resupplyTwo = FilterInserts.calulateResupply()
    resupplyThree = FoodRS.calulateResupply()
    resupplyFour = FoodUS.calulateResupply()
    resupplyFive = KTO.calulateResupply()
    resupplySix = PretreatTanks.calulateResupply()


    print ('Resupply ACY: ', resupplyOne)
    print ('Resupply Filter Inserts: ', resupplyTwo)
    print ('Resupply Food-RS: ', resupplyThree)
    print ('Resupply Food-US: ', resupplyFour)
    print ('Resupply KTO: ', resupplyFive)
    print ('Resupply Pretreat Tanks: ', resupplySix)

    dfOne = ACY.get_resupply_data()
    dfTwo = FilterInserts.get_resupply_data()
    dfThree = FoodRS.get_resupply_data()
    dfFour = FoodUS.get_resupply_data()
    dfFive = KTO.get_resupply_data()
    dfSix = PretreatTanks.get_resupply_data()
    dfCombinedResupply = pd.concat([dfOne, dfTwo, dfThree, dfFour, dfFive, dfSix], ignore_index=True)


    dfOne = ACY.get_category_data()
    dfTwo = FilterInserts.get_category_data()
    dfThree = FoodRS.get_category_data()
    dfFour = FoodUS.get_category_data()
    dfFive = KTO.get_category_data()
    dfSix = PretreatTanks.get_category_data()

    dfOne['Category'] = categoryOne
    dfTwo['Category'] = categoryTwo
    dfThree['Category'] = categoryThree
    dfFour['Category'] = categoryFour
    dfFive['Category'] = categoryFive
    dfSix['Category'] = categorySix


    dfCombined = pd.concat([dfOne, dfTwo, dfThree, dfFour, dfFive, dfSix], ignore_index=True)

    print(dfCombined)
    print(dfCombinedResupply)


    return('success!!!!')

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify
from consumables import Consumables
import pandas as pd
import numpy as np
import json as js
from calculate_consumption_percent_difference import createRequest
from flight_plan import getFlights
from flights import flights
from waterAndGases import waterAndGases
from waterAndGas_consumption import getWaterAndGas
from crews import crews
from crews_query import getCrewCounts

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
        consumables = Consumables()
        results = createRequest(consumables, data)

        print('PRINTING flights_data FROM APP.PY REQUEST:', flights_data)

        # Get the consumables and crew counts for the date range
        consumables_json = results

        #List to make keys for dictionary
        df_list = [consumables_json, UScrew_counts_json, RScrew_counts_json, flights_data]

        frames = {}

        for i, Any in enumerate(df_list):
            frames[f'df{i+1}'] = Any
            newDataJson = js.dumps(frames)

        print('Json string of data: ', newDataJson)

        return jsonify(newDataJson)
    else:
        waterAndGas = waterAndGases()
        results = getWaterAndGas(waterAndGas, data)
        print('You selected water or Gas.', results)
        df_list = [results, UScrew_counts_json, RScrew_counts_json, flights_data]

        frames = {}

        for i, Any in enumerate(df_list):
            frames[f'df{i+1}'] = Any
            newDataJson = js.dumps(frames)

        return jsonify(newDataJson)



if __name__ == "__main__":
    app.run(debug=True)

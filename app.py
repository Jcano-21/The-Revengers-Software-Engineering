from flask import Flask, render_template, request, jsonify
from consumables import Consumables
import pandas as pd
import numpy as np
import json as js
from calculate_consumption_percent_difference import createRequest
from flight_plan import getFlights
from flights import flights

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
    
     # Create an instance of the Consumables class
    consumables = Consumables()
    results = createRequest(consumables, data)

    print('PRINTING flights_data FROM APP.PY REQUEST:', flights_data)

    # Get the consumables and crew counts for the date range
    consumables_data = results['df1']
    UScrew_counts_data = results['df2']
    RScrew_counts_data = results['df3']
    #consumables_data = consumables.get_consumables_for_date_range(data['start_date'], data['end_date'], data['category'])
    #crew_counts_data = consumables.get_Ccount_for_date_range(data['start_date'], data['end_date'])

    #print('consumables_data results:', consumables_data)
    #print('crew_counts_data results:', UScrew_counts_data)
    #print('crew_counts_data results:', RScrew_counts_data)
    consumables_json = consumables_data.to_json(orient='table')
    UScrew_counts_json = UScrew_counts_data.to_json(orient='table')
    RScrew_counts_json = RScrew_counts_data.to_json(orient='table')

    #print('consumables json:', consumables_json)
    #print('crew counts json: ', UScrew_counts_json)
    #print('crew counts json: ', RScrew_counts_json)

    newData = {
            consumables_json,
            UScrew_counts_json,
            RScrew_counts_json
        }

    #print('new Data:', newData)

    df_list = [consumables_json, UScrew_counts_json, RScrew_counts_json, flights_data]

    frames = {}

    for i, Any in enumerate(df_list):
      frames[f'df{i+1}'] = Any
    #print('frames: ', frames)

    newDataJson = js.dumps(frames)

    print('Json string of data: ', newDataJson)

    return jsonify(newDataJson)



if __name__ == "__main__":
    app.run(debug=True)

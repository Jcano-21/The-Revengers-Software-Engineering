import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras.callbacks import EarlyStopping
from keras.optimizers import Adam

import os


def request_modal_update(data_inventory, data_resupply, data_averages):
    # Extract relevant columns from inventory data
    data = data_inventory[['datedim',
                           'distinct_discard_difference', 'Category']]
    # Pivot the table to have categories as columns
    pivot_data = data.pivot(index='datedim', columns='Category',
                            values='distinct_discard_difference').reset_index()

    # Fill missing values with 0 (assuming missing values mean no usage)
    pivot_data.fillna(0, inplace=True)

    # Convert the 'datedim' column to datetime
    pivot_data['datedim'] = pd.to_datetime(pivot_data['datedim'])

    # Set 'datedim' as the index
    pivot_data.set_index('datedim', inplace=True)

    pivot_data['Food-RS'].fillna(0, inplace=True)

    # Normalize the data
    scaler = MinMaxScaler()
    normalized_data = scaler.fit_transform(pivot_data)

    # Prepare data for training
    X, y = [], []
    look_back = 7  # Adjust this based on your data and prediction needs

    for i in range(len(normalized_data) - look_back):
        X.append(normalized_data[i:i+look_back])
        y.append(normalized_data[i+look_back])

    X, y = np.array(X), np.array(y)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=1, shuffle=False)

    # Build the LSTM model
    model = Sequential()
    model.add(LSTM(units=200, input_shape=(
        X_train.shape[1], X_train.shape[2])))
    model.add(Dense(units=len(pivot_data.columns)))
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Define early stopping to prevent overfitting
    early_stopping = EarlyStopping(
        monitor='val_loss', patience=10, restore_best_weights=True)

    # Train the model
    history = model.fit(X_train, y_train, epochs=500, batch_size=100, validation_data=(
        X_test, y_test), callbacks=[early_stopping], verbose=1)

    # Simulate future resupplies
    future_dates = pd.to_datetime(data_resupply['datedim'])
    start_date = '2023-09-06'
    start_date = pd.to_datetime(start_date)
    print(future_dates)
    future_dates = future_dates[(future_dates >= start_date)]

    resupply_amounts = data_averages['USAGE_AVERAGE']
    rate_averages = data_averages['RATE_AVERAGE']
    rate_diff_averages = data_averages['RATE_DIFF_AVERAGE']
    category = {'AYC Inserts', 'Filter Inserts',
                'Food-RS', 'Food-US', 'Pretreat Tanks', 'KTO'}

    for date, amount, rate_avg, rate_diff_avg in zip(future_dates, resupply_amounts, rate_averages, rate_diff_averages):
        print("avg: ", rate_avg)
        print("amount: ", amount)
        # Check if the resupply date exists in the index
        if date in pivot_data.index:
            # Find the index corresponding to the date in the future
            future_index = np.where(pivot_data.index == date)[0][0]

            # Adjust the quantities based on rate averages and rate differences
            pivot_data.iloc[future_index:] += amount

            # Simulate daily usage based on rate averages
            for i in range(future_index, len(pivot_data)):
                pivot_data.iloc[i] -= (rate_avg * 7)

    # Predict future quantities
    future_dates_predict = pd.date_range(start='2023-09-06', end='2025-12-22')
    # Use the last known values as a starting point
    future_data = normalized_data[-look_back:]

    predicted_values = []

    for _ in range(len(future_dates_predict)):
        input_data = np.array([future_data[-look_back:]])
        predicted_value = model.predict(input_data)[0]
        predicted_values.append(predicted_value)
        future_data = np.append(future_data, [predicted_value], axis=0)

    # Inverse transform the predicted values to the original scale
    predicted_values = scaler.inverse_transform(np.array(predicted_values))

    # Create a DataFrame for the predicted values
    predicted_df_LSTM = pd.DataFrame(
        predicted_values, columns=pivot_data.columns, index=future_dates_predict)

    print('Predictions (LSTM with Rates): ', predicted_df_LSTM)
    print("Predicted: ", predicted_values)
    print("Future data: ", future_data)
    print(future_dates)
    print(future_dates_predict)
    return predicted_df_LSTM


def request_modal_update_RSWater(data_inventory, data_resupply, data_averages):
    # Extract relevant columns from inventory data
    data = data_inventory.drop('Category', axis=1)
    # Pivot the table to have categories as columns
    # pivot_data = data.pivot(index='datedim', columns='Category', values='distinct_discard_difference').reset_index()

    print('Resupply data: ', data_averages)

    print('Resupply data: ', data_averages.columns.tolist())

    # Convert the 'datedim' column to datetime
    data['datedim'] = pd.to_datetime(data['datedim'])

    # Set 'datedim' as the index
    data.set_index('datedim', inplace=True)

    print('data inventory: ', data)

    # Normalize the data
    scaler = MinMaxScaler()
    normalized_data = scaler.fit_transform(data)

    # Prepare data for training
    X, y = [], []
    look_back = 7  # Adjust this based on your data and prediction needs

    for i in range(len(normalized_data) - look_back):
        X.append(normalized_data[i:i+look_back])
        y.append(normalized_data[i+look_back])

    X, y = np.array(X), np.array(y)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=1, shuffle=False)

    # Build the LSTM model
    model = Sequential()
    model.add(LSTM(units=50, input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(Dense(units=len(data.columns)))
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Define early stopping to prevent overfitting
    early_stopping = EarlyStopping(
        monitor='val_loss', patience=10, restore_best_weights=True)

    # Train the model
    history = model.fit(X_train, y_train, epochs=50, batch_size=30, validation_data=(
        X_test, y_test), callbacks=[early_stopping], verbose=1)

    # Simulate future resupplies
    future_dates = pd.to_datetime(data_resupply['datedim'])
    start_date = '2023-09-06'
    start_date = pd.to_datetime(start_date)
    print(future_dates)
    future_dates = future_dates[(future_dates >= start_date)]

    resupply_amounts = {'remaining_potableL': data_averages['USAGE_AVERAGE_POT'],
                        'technicalL': data_averages['USAGE_AVERAGE_TECH'], 'rodnik_potableL': data_averages['USAGE_AVERAGE_ROD']}
    rate_averages = {'remaining_potableL': data_averages['RATE_AVERAGE_POT'],
                     'technicalL': data_averages['RATE_AVERAGE_TECH'], 'rodnik_potableL': 0}
    rate_diff_averages = {'remaining_potableL': data_averages['RATE_DIFF_AVERAGE_POT'],
                          'technicalL': data_averages['RATE_DIFF_AVERAGE_TECH'], 'rodnik_potableL': 0}

    for date, amount, rate_avg, rate_diff_avg in zip(future_dates, resupply_amounts, rate_averages, rate_diff_averages):

        print("avg: ", rate_avg)
        print("amount: ", amount)

    # Check if the resupply date exists in the index
    if date in data.index:
        # Find the index corresponding to the date in the future
        future_index = np.where(data.index == date)[0][0]

        # Iterate over columns and adjust quantities based on rate averages and rate differences
        for column in data.columns:
            data[column].iloc[future_index:] += amount[column]

            # Simulate daily usage based on rate averages
            for i in range(future_index, len(data)):
                data[column].iloc[i] -= (rate_avg[column] * 7)

    # Predict future quantities
    future_dates_predict = pd.date_range(start='2023-09-06', end='2025-12-22')
    # Use the last known values as a starting point
    future_data = normalized_data[-look_back:]

    predicted_values = []

    for _ in range(len(future_dates_predict)):
        input_data = np.array([future_data[-look_back:]])
        predicted_value = model.predict(input_data)[0]
        predicted_values.append(predicted_value)
        future_data = np.append(future_data, [predicted_value], axis=0)

    # Inverse transform the predicted values to the original scale
    predicted_values = scaler.inverse_transform(np.array(predicted_values))

    # Create a DataFrame for the predicted values
    predicted_df_LSTM = pd.DataFrame(
        predicted_values, columns=data.columns, index=future_dates_predict)

    print('Predictions (LSTM with Rates): ', predicted_df_LSTM)
    print("Predicted: ", predicted_values)
    print("Future data: ", future_data)
    print(future_dates)
    print(future_dates_predict)
    return predicted_df_LSTM


def request_modal_update_USWater(data_inventory, data_resupply, data_averages):
    # Extract relevant columns from inventory data
    print('Data Invetnory column list: ', data_inventory.columns.tolist())
    data = data_inventory.drop('Category', axis=1)
    # Pivot the table to have categories as columns
    # pivot_data = data.pivot(index='datedim', columns='Category', values='distinct_discard_difference').reset_index()
    data = data.drop('Corrected Predicted (L)', axis=1)

    data = data.drop('resupply_technicalL', axis=1)

    data = data.drop('corrected_totalL', axis=1)

    data = data.drop('resupply_potableL', axis=1)

    print('Resupply data: ', data_averages)

    print('Resupply data: ', data_averages.columns.tolist())

    # Convert the 'datedim' column to datetime
    data['datedim'] = pd.to_datetime(data['datedim'])

    # Set 'datedim' as the index
    data.set_index('datedim', inplace=True)

    print('data inventory: ', data)

    # Normalize the data
    scaler = MinMaxScaler()
    normalized_data = scaler.fit_transform(data)

    # Prepare data for training
    X, y = [], []
    look_back = 7  # Adjust this based on your data and prediction needs

    for i in range(len(normalized_data) - look_back):
        X.append(normalized_data[i:i+look_back])
        y.append(normalized_data[i+look_back])

    X, y = np.array(X), np.array(y)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=1, shuffle=False)

    # Build the LSTM model
    model = Sequential()
    model.add(LSTM(units=50, input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(Dense(units=len(data.columns)))
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Define early stopping to prevent overfitting
    early_stopping = EarlyStopping(
        monitor='val_loss', patience=10, restore_best_weights=True)

    # Train the model
    history = model.fit(X_train, y_train, epochs=50, batch_size=30, validation_data=(
        X_test, y_test), callbacks=[early_stopping], verbose=1)

    # Simulate future resupplies
    future_dates = pd.to_datetime(data_resupply['datedim'])
    start_date = '2023-09-06'
    start_date = pd.to_datetime(start_date)
    print(future_dates)
    future_dates = future_dates[(future_dates >= start_date)]

    resupply_amounts = {
        'corrected_potableL': data_averages['USAGE_AVERAGE_POT'], 'corrected_technicalL': data_averages['USAGE_AVERAGE_TECH']}
    rate_averages = {'corrected_potableL': data_averages['RATE_AVERAGE_POT'],
                     'corrected_technicalL': data_averages['RATE_AVERAGE_TECH']}
    rate_diff_averages = {
        'corrected_potableL': data_averages['RATE_DIFF_AVERAGE_POT'], 'corrected_technicalL': data_averages['RATE_DIFF_AVERAGE_TECH']}

    for date, amount, rate_avg, rate_diff_avg in zip(future_dates, resupply_amounts, rate_averages, rate_diff_averages):

        print("avg: ", rate_avg)
        print("amount: ", amount)

    # Check if the resupply date exists in the index
    if date in data.index:
        # Find the index corresponding to the date in the future
        future_index = np.where(data.index == date)[0][0]

        # Iterate over columns and adjust quantities based on rate averages and rate differences
        for column in data.columns:
            data[column].iloc[future_index:] += amount[column]

            # Simulate daily usage based on rate averages
            for i in range(future_index, len(data)):
                data[column].iloc[i] -= (rate_avg[column] * 7)

    # Predict future quantities
    future_dates_predict = pd.date_range(start='2023-09-06', end='2025-12-22')
    # Use the last known values as a starting point
    future_data = normalized_data[-look_back:]

    predicted_values = []

    for _ in range(len(future_dates_predict)):
        input_data = np.array([future_data[-look_back:]])
        predicted_value = model.predict(input_data)[0]
        predicted_values.append(predicted_value)
        future_data = np.append(future_data, [predicted_value], axis=0)

    # Inverse transform the predicted values to the original scale
    predicted_values = scaler.inverse_transform(np.array(predicted_values))

    # Create a DataFrame for the predicted values
    predicted_df_LSTM = pd.DataFrame(
        predicted_values, columns=data.columns, index=future_dates_predict)

    print('Predictions (LSTM with Rates): ', predicted_df_LSTM)
    print("Predicted: ", predicted_values)
    print("Future data: ", future_data)
    print(future_dates)
    print(future_dates_predict)
    return predicted_df_LSTM


def request_modal_update_Gas(data_inventory, data_resupply, data_averages):
    print('data inventor : ', data_inventory)
    # Extract relevant columns from inventory data
    print('Data Invetnory column list: ', data_inventory.columns.tolist())
    data = data_inventory.drop('Category', axis=1)

    data['newO2kg'] = data['US_O2kg'] + data['RS_O2kg']
    data['newN2kg'] = data['US_N2kg'] + data['RS_N2kg']

    data = data.drop('US_O2kg', axis=1)
    data = data.drop('RS_O2kg', axis=1)
    data = data.drop('US_N2kg', axis=1)
    data = data.drop('RS_N2kg', axis=1)
    data = data.drop('adjusted_O2kg', axis=1)
    data = data.drop('adjusted_N2kg', axis=1)
    data = data.drop('resupply_O2kg', axis=1)
    data = data.drop('resupply_N2kg', axis=1)
    data = data.drop('resupply_air_kg', axis=1)

    print('Resupply data: ', data_averages)

    print('Resupply data: ', data_averages.columns.tolist())

    # Convert the 'datedim' column to datetime
    data['datedim'] = pd.to_datetime(data['datedim'])

    # Set 'datedim' as the index
    data.set_index('datedim', inplace=True)

    print('data inventory: ', data['newO2kg'])

    # Normalize the data
    scaler = MinMaxScaler()
    normalized_data = scaler.fit_transform(data)

    # Prepare data for training
    X, y = [], []
    look_back = 7  # Adjust this based on your data and prediction needs

    for i in range(len(normalized_data) - look_back):
        X.append(normalized_data[i:i+look_back])
        y.append(normalized_data[i+look_back])

    X, y = np.array(X), np.array(y)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=1, shuffle=False)

    # Build the LSTM model
    model = Sequential()
    model.add(LSTM(units=500, input_shape=(
        X_train.shape[1], X_train.shape[2])))
    model.add(Dense(units=len(data.columns)))
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Define early stopping to prevent overfitting
    early_stopping = EarlyStopping(
        monitor='val_loss', patience=10, restore_best_weights=True)

    # Train the model
    history = model.fit(X_train, y_train, epochs=50, batch_size=8, validation_data=(
        X_test, y_test), callbacks=[early_stopping], verbose=1)

    # Simulate future resupplies
    future_dates = pd.to_datetime(data_resupply['datedim'])
    start_date = '2023-09-06'
    start_date = pd.to_datetime(start_date)
    print(future_dates)
    future_dates = future_dates[(future_dates >= start_date)]

    future_data = pd.DataFrame(index=future_dates, columns=data.columns)

    # Concatenate the original DataFrame and the DataFrame with 'Future Index'
    # data = pd.concat([data, future_data])

    # Sort the index to maintain order
    data.sort_index(inplace=True)

    print('New data: ', data)

    resupply_amounts = {
        'newO2kg': data_averages['USAGE_AVERAGE_O2'], 'newN2kg': data_averages['USAGE_AVERAGE_N2']}
    rate_averages = {
        'newO2kg': data_averages['RATE_AVERAGE_O2'], 'newN2kg': data_averages['RATE_AVERAGE_N2']}
    rate_diff_averages = {
        'newO2kg': data_averages['RATE_DIFF_AVERAGE_O2'], 'newN2kg': data_averages['RATE_DIFF_AVERAGE_N2']}

    print('FUTURE DATES: ', future_dates)

    for date in future_dates:

        print('This is the date: ', date)

        # Check if the resupply date exists in the index
        if date in data.index:
            # Find the index corresponding to the date in the future

            future_index = np.where(data.index == date)[0][0]

            # Iterate over columns and adjust quantities based on rate averages and rate differences
            for column in data.columns:
                if column == 'newO2kg':
                    newAmount = data_averages['RESUPPLY_AVERAGE_O2']
                elif column == 'newN2kg':
                    newAmount = data_averages['RESUPPLY_AVERAGE_N2']
                print(column)
                print(data[column].iloc[future_index:])
                data[column].iloc[future_index] = 0.0
                print(data[column].iloc[future_index:])
                data[column].iloc[future_index] += newAmount

                # Simulate daily usage based on rate averages
                # for i in range(future_index, len(data)):
                #    data[column].iloc[i] -= (rate_avg * 7)

    print('maybe future here: ', data)

    # Predict future quantities
    future_dates_predict = pd.date_range(start='2023-09-06', end='2025-12-22')
    # Use the last known values as a starting point
    future_data = normalized_data[-look_back:]

    predicted_values = []

    for _ in range(len(future_dates_predict)):
        input_data = np.array([future_data[-look_back:]])
        predicted_value = model.predict(input_data)[0]
        predicted_values.append(predicted_value)
        future_data = np.append(future_data, [predicted_value], axis=0)

    # Inverse transform the predicted values to the original scale
    predicted_values = scaler.inverse_transform(np.array(predicted_values))

    # Create a DataFrame for the predicted values
    predicted_df_LSTM = pd.DataFrame(predicted_values, columns=data.columns)
    predicted_df_LSTM = predicted_df_LSTM.iloc[::7]
    # Set the index based on the weekly intervals
    predicted_df_LSTM.index = future_dates_predict[::7]

    print('Predictions (LSTM with Rates): ', predicted_df_LSTM)
    print("Predicted: ", predicted_values)
    print("Future data: ", future_data)
    print(future_dates)
    print(future_dates_predict)
    return predicted_df_LSTM

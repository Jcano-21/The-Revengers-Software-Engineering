import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras.callbacks import EarlyStopping
import os

def request_modal_update(data_inventory, data_resupply, data_averages):
    # Extract relevant columns from inventory data
    data = data_inventory[['datedim', 'distinct_discard_difference', 'Category']]

    # Pivot the table to have categories as columns
    pivot_data = data.pivot(index='datedim', columns='Category', values='distinct_discard_difference').reset_index()

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
    look_back = 70  # Adjust this based on your data and prediction needs

    for i in range(len(normalized_data) - look_back):
        X.append(normalized_data[i:i+look_back])
        y.append(normalized_data[i+look_back])

    X, y = np.array(X), np.array(y)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1, shuffle=False)

    # Build the LSTM model
    model = Sequential()
    model.add(LSTM(units=50, input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(Dense(units=len(pivot_data.columns)))
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Define early stopping to prevent overfitting
    early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

    # Train the model
    history = model.fit(X_train, y_train, epochs=15, batch_size=30, validation_data=(X_test, y_test), callbacks=[early_stopping], verbose=1)

    # # Plot training history
    # plt.plot(history.history['loss'], label='Train Loss')
    # plt.plot(history.history['val_loss'], label='Validation Loss')
    # plt.legend()
    # plt.show()

    # Simulate future resupplies
    future_dates = pd.to_datetime(data_resupply['datedim'])
    start_date = '2023-09-06'
    start_date = pd.to_datetime(start_date)
    print(future_dates)
    future_dates = future_dates[(future_dates >= start_date)]

    resupply_amounts = data_averages['USAGE_AVERAGE']
    rate_averages = data_averages['RATE_AVERAGE']
    rate_diff_averages = data_averages['RATE_DIFF_AVERAGE']
    category = { 'AYC Inserts', 'Filter Inserts', 'Food-RS', 'Food-US', 'Pretreat Tanks', 'KTO'}

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
    future_data = normalized_data[-look_back:]  # Use the last known values as a starting point

    predicted_values = []

    for _ in range(len(future_dates_predict)):
        input_data = np.array([future_data[-look_back:]])
        predicted_value = model.predict(input_data)[0]
        predicted_values.append(predicted_value)
        future_data = np.append(future_data, [predicted_value], axis=0)

    # Inverse transform the predicted values to the original scale
    predicted_values = scaler.inverse_transform(np.array(predicted_values))

    # Create a DataFrame for the predicted values
    predicted_df_LSTM = pd.DataFrame(predicted_values, columns=pivot_data.columns, index=future_dates_predict)
    output_directory = "C:/Users/zakar/Documents/output/"
    os.makedirs(output_directory, exist_ok=True)
    predicted_df_LSTM.to_csv(os.path.join(output_directory, "LSTM_with_rates.csv"))

    # # Plot the predictions
    # plt.figure(figsize=(12, 6))
    # for category in pivot_data.columns:
    #     plt.plot(pivot_data.index, pivot_data[category], label=f'Actual - {category}')
    #     plt.plot(predicted_df_LSTM.index, predicted_df_LSTM[category], label=f'Predicted - {category}', linestyle='dashed')

    # plt.title('Future Quantities Prediction (LSTM with Rates)')
    # plt.xlabel('Date')
    # plt.ylabel('Quantity')
    # plt.legend()
    # plt.show()

    print('Predictions (LSTM with Rates): ', predicted_df_LSTM)
    print ("Predicted: ", predicted_values)
    print("Future data: ", future_data)
    print(future_dates) 
    print(future_dates_predict)
    return predicted_df_LSTM

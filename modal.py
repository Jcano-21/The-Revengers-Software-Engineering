import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from consumables import Consumables

import pandas as pd

def request_modal_update(df_consumables, df_flight_plan, df_resupply_quantities):
    
    Merge flight plan and resupply quantities data
    merged_data = pd.merge(df_flight_plan, df_resupply_quantities, on=['datedim', 'event'], how='left')

    #Filter for resupply events
    resupply_data = merged_data[merged_data['event'] == 'resupply']

    # Combine the total between RSA and NASA for each category
    resupply_data['total_quantity'] = resupply_data.groupby('category')['distinct_discard_difference'].transform('sum')


    # Convert the results to JSON
    dateOneJson = json.loads(dateOne)

    #Extracting features and target variable
    features = df_consumables[['nasa_count', 'rsa00_count', 'distinct_id_count_categories', 'discard_count']]
    target = df_consumables['distinct_discard_difference']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

    # Standardize the features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Build the neural network model
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(1, activation='linear')  # Linear activation for regression
    ])

    # Compile the model
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

    # Train the model
    model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))

    # Evaluate the model
    loss, mae = model.evaluate(X_test, y_test)
    print(f'Mean Absolute Error on Test Set: {mae}')

    # Make predictions
    predictions = model.predict(X_test)

    # 
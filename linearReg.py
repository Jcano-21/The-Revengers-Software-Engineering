import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer

def request_modal_LR_update(inventory_data, future_resupply, averages):
    # Merge inventory_data with averages
    merged_data = pd.merge(inventory_data, averages, on='Category')

    # Set the date column as the index
    merged_data['datedim'] = pd.to_datetime(merged_data['datedim'])
    merged_data.set_index('datedim', inplace=True)

    # Feature Engineering
    # Create lag values for quantities
    for category in merged_data['Category'].unique():
        merged_data[f'{category}_lag'] = merged_data.groupby('Category')['distinct_discard_difference'].shift()

    # Use RATE_AVERAGES and RESUPPLY_AVERAGES in your feature engineering
    # For example, you might use them to create features like 'consumption_rate' and 'resupply_quantity'
    merged_data['consumption_rate'] = merged_data['RATE_AVERAGE']  # Replace 'RATE_AVERAGES' with the actual column name
    merged_data['resupply_quantity'] = merged_data['RESUPPLY_AVERAGE']  # Replace 'RESUPPLY_AVERAGES' with the actual column name

    # Train the model on the entire dataset
    X_train = merged_data.drop(['distinct_discard_difference', 'Category'], axis=1)
    y_train = merged_data['distinct_discard_difference']

    # Impute missing values
    imputer = SimpleImputer(strategy='mean')
    X_train_imputed = imputer.fit_transform(X_train)

    # Get the feature names from the training data
    feature_names = X_train.columns

    # Replace RandomForestRegressor with your preferred model
    model = RandomForestRegressor()
    model.fit(X_train_imputed, y_train)

    # Future Prediction
    # Use RATE_AVERAGES and RESUPPLY_AVERAGES for feature engineering in future_data
    future_data = pd.DataFrame(index=future_resupply['datedim'])
    future_data['consumption_rate'] = averages['RATE_AVERAGE'].values[0]  # Replace 'RATE_AVERAGES' with the actual column name
    future_data['resupply_quantity'] = averages['RESUPPLY_AVERAGE'].values[0]  # Replace 'RESUPPLY_AVERAGES' with the actual column name

    # Ensure the order of columns in future_data matches the order during model training
    # Assuming you have these columns in your future_data DataFrame, adjust as needed
    print(future_data)
    additional_columns = ['distinct_id_count_categories', 'discard_count', 'RATE_AVERAGE', 'RATE_DIFF_AVERAGE', 'DAYS_BETWEEN_RESUPPLY_AVERAGE', 'USAGE_AVERAGE', 'RESUPPLY_AVERAGE', 'ACY Inserts_lag', 'Filter Inserts_lag', 'Food-RS_lag', 'Food-US_lag', 'KTO_lag', 'Pretreat Tanks_lag']
    future_data = future_data[additional_columns]

    # Impute missing values for future data
    future_data_imputed = imputer.transform(future_data)

    # Set feature names for the imputed future data
    future_data_imputed = pd.DataFrame(future_data_imputed, columns=additional_columns, index=future_data.index)

    # Use the trained model to predict future quantities
    future_predictions = model.predict(future_data_imputed)

    # Create a DataFrame for the predicted values
    predicted_df_imputed = pd.DataFrame(future_predictions, columns=['Predicted_Quantity'], index=future_data.index)

    # Plot the results with imputed data
    predicted_df_imputed.plot(figsize=(12, 6), title='Predicted Quantities for Future Dates')

    print('Imputed Predictions: ', predicted_df_imputed)

    return

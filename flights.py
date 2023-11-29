import pandas as pd

class flights:

    def __init__(self):
        self._flight_data = {}  # Private attribute
        
    def _calculate_something(self):
        # A private method for data calculation
        pass

    def load_flights_data(self, df):
        self._flights_data = df

    def get_flight_data(self):
        df = self._flights_data
        return df

    def get_flights_for_date_range(self, start_date, end_date):
        print("Date Range - Start Date:", start_date)
        print("Date Range - End Date:", end_date)

        flights_info = None

        # Check if the specified category exists in the category data
        
        # Filter category_info based on category
        flights_info = self._flights_data

        # Ensure 'datedim' column is in datetime format
        flights_info['datedim'] = pd.to_datetime(flights_info['datedim'])

        # Convert start_date and end_date to datetime format
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        # Filter based on date range
        flights_info = flights_info[(flights_info['datedim'] >= start_date) & (flights_info['datedim'] <= end_date)]

        # Add print statements to display the results
        print("Flights Info:")
        print(flights_info)

        return flights_info

    
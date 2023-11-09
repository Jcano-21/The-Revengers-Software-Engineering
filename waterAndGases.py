import pandas as pd

class waterAndGases:

    def __init__(self):
        self._RSWater_data = {}  # Private attribute
        self._USWater_data = {}  # Private attribute
        self._Gas_data = {}  # Private attribute


        
    def _calculate_something(self):
        # A private method for data calculation
        pass

    def load_RSWater_data(self, df):
        self._RSWater_data = df

    def load_USWater_data(self, df):
        self._USWater_data = df

    def load_Gas_data(self, df):
        self._Gas_data = df


    def get_RSWater_for_date_range(self, start_date, end_date):
        print("Date Range - Start Date:", start_date)
        print("Date Range - End Date:", end_date)

        RSWater_info = None

        # Check if the specified category exists in the category data
        
        # Store RSWater_data
        RSWater_info = self._RSWater_data

        # Ensure 'datedim' column is in datetime format
        RSWater_info['datedim'] = pd.to_datetime(RSWater_info['datedim'])

        # Convert start_date and end_date to datetime format
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        # Filter based on date range
        RSWater_info = RSWater_info[(RSWater_info['datedim'] >= start_date) & (RSWater_info['datedim'] <= end_date)]

        # Add print statements to display the results
        print("Flights Info:")
        print(RSWater_info)

        return RSWater_info

    def get_USWater_for_date_range(self, start_date, end_date):
        print("Date Range - Start Date:", start_date)
        print("Date Range - End Date:", end_date)

        USWater_info = None

        # Check if the specified category exists in the category data
        
        # Store USWater_data
        USWater_info = self._USWater_data

        # Ensure 'datedim' column is in datetime format
        USWater_info['datedim'] = pd.to_datetime(USWater_info['datedim'])

        # Convert start_date and end_date to datetime format
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        # Filter based on date range
        USWater_info = USWater_info[(USWater_info['datedim'] >= start_date) & (USWater_info['datedim'] <= end_date)]

        # Add print statements to display the results
        print("Flights Info:")
        print(USWater_info)

        return USWater_info
    

    def get_Gas_for_date_range(self, start_date, end_date):
        print("Date Range - Start Date:", start_date)
        print("Date Range - End Date:", end_date)

        Gas_info = None

        # Check if the specified category exists in the category data
        
        # Store Gas_data
        Gas_info = self._Gas_data

        # Ensure 'datedim' column is in datetime format
        Gas_info['datedim'] = pd.to_datetime(Gas_info['datedim'])

        # Convert start_date and end_date to datetime format
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        # Filter based on date range
        Gas_info = Gas_info[(Gas_info['datedim'] >= start_date) & (Gas_info['datedim'] <= end_date)]

        # Add print statements to display the results
        print("Flights Info:")
        print(Gas_info)

        return Gas_info
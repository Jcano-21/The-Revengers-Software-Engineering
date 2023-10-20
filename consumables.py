import pandas as pd

class Consumables:
    def __init__(self):
        self._category_data = {}  # Private attribute
        self._RS_crew_count = {}  # Private attribute for RS crew count
        self._US_crew_count = {}  # Private attribute for US crew count

    def _calculate_something(self):
        # A private method for data calculation
        pass

    def load_category_data(self, category, df):
        self._category_data[category] = df

    def load_RS_crew_count(self, df):
        self._RS_crew_count = df

    def load_US_crew_count(self, df):
        self._US_crew_count = df

    def get_consumables_for_date(self, date, category):
        print("Category:", category)
        print("Date:", date)

        category_info = None
        
        # Check if the specified category exists in the category data
        if category in self._category_data:
            # Filter category_info based on date and category
            category_info = self._category_data[category]

            # Ensure 'datedim' column is in datetime format
            category_info['datedim'] = pd.to_datetime(category_info['datedim'])

            # Convert date_to_get_info to datetime format
            date_to_get_info = pd.to_datetime(date)

            # Filter based on date
            category_info = category_info[category_info['datedim'] == date_to_get_info]

        # Add print statements to display the results
        print("Category Info:")
        print(category_info)
        
        return category_info

    def get_Ccount_for_date(self, date):
        print("Date:", date)

    
        RS_crew_info = None
        US_crew_info = None

        # Convert date_to_get_info to datetime format
        date_to_get_info = pd.to_datetime(date)

        if self._RS_crew_count is not None:
            RS_crew_info = self._RS_crew_count

            # Ensure 'datedim' column is in datetime format
            RS_crew_info['datedim'] = pd.to_datetime(RS_crew_info['datedim'])

            # Filter based on date
            RS_crew_info = RS_crew_info[RS_crew_info['datedim'] == date_to_get_info]

        if self._US_crew_count is not None:
            US_crew_info = self._US_crew_count

            # Ensure 'datedim' column is in datetime format
            US_crew_info['datedim'] = pd.to_datetime(US_crew_info['datedim'])

            # Filter based on date
            US_crew_info = US_crew_info[US_crew_info['datedim'] == date_to_get_info]

        print("RS Crew Information:")
        print(RS_crew_info)

        print("US Crew Information:")
        print(US_crew_info)

        return RS_crew_info, US_crew_info

# Usage:
# consumables = Consumables()
# Load data and crew counts using load_category_data, load_RS_crew_count, and load_US_crew_count
# Get info for a date using get_info_for_date

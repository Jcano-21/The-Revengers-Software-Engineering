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


    def get_consumables_for_date_range(self, start_date, end_date, category):
        print("Category:", category)
        print("Date Range - Start Date:", start_date)
        print("Date Range - End Date:", end_date)

        category_info = None

        # Check if the specified category exists in the category data
        if category in self._category_data:
            # Filter category_info based on category
            category_info = self._category_data[category]

            # Ensure 'datedim' column is in datetime format
            category_info['datedim'] = pd.to_datetime(category_info['datedim'])

            # Convert start_date and end_date to datetime format
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)

            # Filter based on date range
            category_info = category_info[(category_info['datedim'] >= start_date) & (category_info['datedim'] <= end_date)]

        # Add print statements to display the results
        print("Category Info:")
        print(category_info)

        return category_info

    def get_Ccount_for_date_range(self, start_date, end_date):
        print("Date Range - Start Date:", start_date)
        print("Date Range - End Date:", end_date)

        RS_crew_info = None
        US_crew_info = None

        # Convert start_date and end_date to datetime format
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        if self._RS_crew_count is not None:
            RS_crew_info = self._RS_crew_count

            # Ensure 'datedim' column is in datetime format
            RS_crew_info['datedim'] = pd.to_datetime(RS_crew_info['datedim'])

            # Filter based on date range
            RS_crew_info = RS_crew_info[(RS_crew_info['datedim'] >= start_date) & (RS_crew_info['datedim'] <= end_date)]

        if self._US_crew_count is not None:
            US_crew_info = self._US_crew_count

            # Ensure 'datedim' column is in datetime format
            US_crew_info['datedim'] = pd.to_datetime(US_crew_info['datedim'])

            # Filter based on date range
            US_crew_info = US_crew_info[(US_crew_info['datedim'] >= start_date) & (US_crew_info['datedim'] <= end_date)]

        print("RS Crew Information:")
        print(RS_crew_info)

        print("US Crew Information:")
        print(US_crew_info)

        return RS_crew_info, US_crew_info


    
import pandas as pd
import json


class Consumables:
    def __init__(self):
        self._category_data = {}  # Private attribute
        self._RS_crew_count = {}  # Private attribute for RS crew count
        self._US_crew_count = {}  # Private attribute for US crew count

    def calculate_something(self, start_date, end_date, category, crewData):
        # A private method for data calculation
        # Filter category_info based on category
            category_info = self._category_data[category]
            print('start date: ', category_info)


            # Ensure 'datedim' column is in datetime format
            category_info['datedim'] = pd.to_datetime(category_info['datedim'])

            # Convert start_date and end_date to datetime format
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)

            # Filter based on date range
            newStart = category_info.datedim.iloc[0]
            start_date_consumption = category_info[(category_info['datedim'] == newStart)]
            print('debug print: ', start_date_consumption)
            end_date_consumption = category_info[(category_info['datedim'] == end_date)]
            difference_consumption = (end_date_consumption.discard_count.iloc[0] + end_date_consumption.discard_count.iloc[1]) - (start_date_consumption.discard_count.iloc[0] + start_date_consumption.discard_count.iloc[1])
            print('DATES !!!!!!!!!!!!!!', start_date_consumption, end_date_consumption)
            print('DIFFERENCE between dates: ', difference_consumption)
            print('HEre is the category: ', category)
            if category == 'Filter Inserts':
                rates = 0.007575758
            elif category == 'ACY Inserts':
                rates = 1.3
            elif category == 'Food-RS':
                rates = 0.2
            elif category == 'Food-US':
                rates = 0.027
            elif category == 'KTO':
                rates = 0.035714286
            elif category == 'Pretreat Tanks':
                rates = 0.005555556

            difference_in_days = (end_date_consumption.datedim.iloc[1]) - (start_date_consumption.datedim.iloc[0])
            print('Difference in Days: ', (end_date_consumption.datedim.iloc[1]), ' : ', (start_date_consumption.datedim.iloc[0]), ' : ', difference_in_days.days, ' Days')
            calculated_consumption = ((difference_consumption / difference_in_days.days) / 7)
            print('Calculated Consumption Rate: ', calculated_consumption)
            print('Here is the current Rate: ', rates)

            percent_difference = ((calculated_consumption - rates) * 100) / rates 
            print('PERCENT DIFFERENCE IN RATES: ', percent_difference)
            consumption_data = {'rate': rates, 'calculated_rate': calculated_consumption, 'Percent_Difference': percent_difference}
            json_consumption_data = json.dumps(consumption_data)
            print('percent difference json: ', json_consumption_data)
            return json_consumption_data 

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


    
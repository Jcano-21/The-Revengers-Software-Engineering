import pandas as pd
import json

class waterAndGases:

    def __init__(self):
        self._RSWater_data = {}  # Private attribute
        self._USWater_data = {}  # Private attribute
        self._Gas_data = {}  # Private attribute


        
    def calculate_US_water(self, start_date, end_date):
        # Filter category_info based on category
            USWater_info = self._USWater_data
            print('start date: ', USWater_info)


            # Ensure 'datedim' column is in datetime format
            USWater_info['datedim'] = pd.to_datetime(USWater_info['datedim'])

            # Convert start_date and end_date to datetime format
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)

            # Filter based on date range
            newStart = USWater_info.datedim.iloc[0]
            start_date_consumption = USWater_info[(USWater_info['datedim'] == start_date)]

            if start_date_consumption.empty:
                start_date_consumption = USWater_info[(USWater_info['datedim'] == newStart)]

            end_date_consumption = USWater_info[(USWater_info['datedim'] == end_date)]
            if end_date_consumption.empty:
                end_date_consumption = USWater_info[(USWater_info['datedim'] == USWater_info.datedim.iloc[-1])]
            difference_consumption = start_date_consumption.corrected_potableL.iloc[0]  - end_date_consumption.corrected_potableL.iloc[-1]
            difference_consumption_technical = start_date_consumption.corrected_technicalL.iloc[0]  - end_date_consumption.corrected_technicalL.iloc[-1]
            print('DATES:', start_date_consumption, end_date_consumption)
            print('DIFFERENCE between dates: ', difference_consumption)
            ratesPot = 2.844
            ratesTech = 11.5
                
            difference_in_days = (end_date_consumption.datedim.iloc[-1]) - (start_date_consumption.datedim.iloc[0])
            print('Difference in Days: ', (end_date_consumption.datedim.iloc[-1]), ' : ', (start_date_consumption.datedim.iloc[0]), ' : ', difference_in_days.days, ' Days')
            calculated_consumption = ((difference_consumption / difference_in_days.days) / 4)
            calculated_consumption_tech = (((difference_consumption_technical + (10.435 * difference_in_days.days)) / difference_in_days.days))
            print('Calculated Consumption Rate: ', calculated_consumption)
            print('Here is the current Rate: ', ratesPot)
            print('Calculated Consumption Rate Tech: ', calculated_consumption_tech)
            print('Here is the current Rate: ', ratesTech)
            percent_difference = ((calculated_consumption - ratesPot) * 100) / ratesPot 
            percent_difference_tech = ((calculated_consumption_tech - ratesTech) * 100) / ratesTech 

            print('PERCENT DIFFERENCE IN RATES: ', percent_difference)
            print('PERCENT DIFFERENCE IN RATESTECH: ', percent_difference_tech)

            consumption_data = {'rate': ratesPot, 'calculated_rate': calculated_consumption, 'Percent_Difference': percent_difference,
             'rateTech': ratesTech, 'calculated_rate_tech': calculated_consumption_tech, 'Percent_DifferenceTech': percent_difference_tech}
            print('Consumption_data: ', consumption_data)
            json_consumption_data = json.dumps(consumption_data)
            print('percent difference json: ', json_consumption_data)
            return json_consumption_data 

    def calculate_RS_water(self, start_date, end_date):
        # Filter category_info based on category
            RSWater_info = self._RSWater_data
            print('start date: ', RSWater_info)


            # Ensure 'datedim' column is in datetime format
            RSWater_info['datedim'] = pd.to_datetime(RSWater_info['datedim'])

            # Convert start_date and end_date to datetime format
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)

            # Filter based on date range
            newStart = RSWater_info.datedim.iloc[0]
            start_date_consumption = RSWater_info[(RSWater_info['datedim'] == start_date)]

            if start_date_consumption.empty:
                start_date_consumption = RSWater_info[(RSWater_info['datedim'] == newStart)]

            end_date_consumption = RSWater_info[(RSWater_info['datedim'] == end_date)]
            if end_date_consumption.empty:
                end_date_consumption = RSWater_info[(RSWater_info['datedim'] == RSWater_info.datedim.iloc[-1])]
            difference_consumption = start_date_consumption.remaining_potableL.iloc[0]  - end_date_consumption.remaining_potableL.iloc[-1]
            difference_consumption_technical = start_date_consumption.technicalL.iloc[0]  - end_date_consumption.technicalL.iloc[-1]
            print('DATES: ', start_date_consumption, end_date_consumption)
            print('DIFFERENCE between dates: ', difference_consumption)
            ratesPot = 2.5
            ratesTech = 11.5
                
            difference_in_days = (end_date_consumption.datedim.iloc[-1]) - (start_date_consumption.datedim.iloc[0])
            print('Difference in Days: ', (end_date_consumption.datedim.iloc[-1]), ' : ', (start_date_consumption.datedim.iloc[0]), ' : ', difference_in_days.days, ' Days')
            calculated_consumption = (((difference_consumption + (2.68 * difference_in_days.days)) / difference_in_days.days) / 4)
            calculated_consumption_tech = (((difference_consumption_technical + (10.435 * difference_in_days.days)) / difference_in_days.days))
            print('Calculated Consumption Rate: ', calculated_consumption)
            print('Here is the current Rate: ', ratesPot)
            print('Calculated Consumption Rate Tech: ', calculated_consumption_tech)
            print('Here is the current Rate: ', ratesTech)
            percent_difference = ((calculated_consumption - ratesPot) * 100) / ratesPot 
            percent_difference_tech = ((calculated_consumption_tech - ratesTech) * 100) / ratesTech 

            print('PERCENT DIFFERENCE IN RATES: ', percent_difference)
            print('PERCENT DIFFERENCE IN RATESTECH: ', percent_difference_tech)

            consumption_data = {'rate': ratesPot, 'calculated_rate': calculated_consumption, 'Percent_Difference': percent_difference,
             'rateTech': ratesTech, 'calculated_rate_tech': calculated_consumption_tech, 'Percent_DifferenceTech': percent_difference_tech}
            print('Consumption_data: ', consumption_data)
            json_consumption_data = json.dumps(consumption_data)
            print('percent difference json: ', json_consumption_data)
            return json_consumption_data 

        

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
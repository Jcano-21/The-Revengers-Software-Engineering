import pandas as pd
import json
import numpy as np 
import datetime
from datetime import timedelta



class Consumables:
    def __init__(self, category):
        self._category_data = {}  # Private attribute
        self._RS_crew_count = {}  # Private attribute for RS crew count
        self._US_crew_count = {}  # Private attribute for US crew count
        self._resupply_dates = {}
        self._category = category
        self._resupply_data = {}
        self.flights = {}
        
    def load_category_data(self, df):
        self._category_data = df

    def load_RS_crew_count(self, df):
        self._RS_crew_count = df

    def load_US_crew_count(self, df):
        self._US_crew_count = df
    
    def load_resupply_dates(self, df):
        self._resupply_dates = df
        
    def load_resupply_data(self, df):
        self._resupply_data = df

    def load_flights_data(self, df):
        self.flights = df
        

    def get_consumables_for_date_range(self, start_date, end_date, category):
        print("Category:", category)
        print("Date Range - Start Date:", start_date)
        print("Date Range - End Date:", end_date)

        category_info = None

        # Check if the specified category exists in the category data
        #if category in self._category_data:
            # Filter category_info based on category
        category_info = self._category_data

        # Ensure 'datedim' column is in datetime format
        category_info['datedim'] = pd.to_datetime(category_info['datedim'])

        # Convert start_date and end_date to datetime format
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        # Filter based on date range
        category_info = category_info[(category_info['datedim'] >= start_date) & (category_info['datedim'] <= end_date)]
        rs_consumables = category_info[(category_info['current_ip_owner'] == 'RSA00')] 
        us_consumables = category_info[(category_info['current_ip_owner'] == 'NASA')]
        
        # Merge the two DataFrames on 'datedim'
        merged_df = pd.merge(rs_consumables, us_consumables, on='datedim', suffixes=('_df1', '_df2'))

        # Sum the count columns
        merged_df['nasa_count'] = merged_df['nasa_count_df1'] + merged_df['nasa_count_df2']
        merged_df['rsa00_count'] = merged_df['rsa00_count_df1'] + merged_df['rsa00_count_df2']
        merged_df['distinct_id_count_categories'] = merged_df['distinct_id_count_categories_df1'] + merged_df['distinct_id_count_categories_df2']
        merged_df['discard_count'] = merged_df['discard_count_df1'] + merged_df['discard_count_df2']
        merged_df['distinct_discard_difference'] = merged_df['distinct_discard_difference_df1'] + merged_df['distinct_discard_difference_df2']

        # Select only the relevant columns
        result_df = merged_df[['datedim', 'distinct_id_count_categories', 'discard_count', 'distinct_discard_difference']]

        print("MERGED DATAFRAME: ", result_df)

        print("Category Info:") 
        print(category_info)

        print("RS CONSUMABLES: ", rs_consumables)
        print("US CONSUMBABLES: ", us_consumables)
        print("MERGED DATAFRAME: ", result_df)

        return rs_consumables, us_consumables, result_df

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
    
    def calculate_something(self, start_date_, end_date, category, crewData):
        # A private method for data calculation
        # Filter category_info based on category
            category_info = self._category_data
            print('start date: ', category_info)


            # Ensure 'datedim' column is in datetime format
            category_info['datedim'] = pd.to_datetime(category_info['datedim'])

            # Convert start_date and end_date to datetime format
            start_date = pd.to_datetime(start_date_)
            end_date = pd.to_datetime(end_date)
            resupply_quantity_date = end_date + pd.DateOffset(days=1)
            print('Resupply Date: !!!!!', resupply_quantity_date, 'previous day: ', end_date)
            

            # Filter based on date range
            newStart = category_info.datedim.iloc[0]
            start_date_consumption = category_info[(category_info['datedim'] == start_date)]
            print('debug print BEFORE IF: ', start_date_consumption)
            if start_date_consumption.empty:
                start_date_consumption = category_info[(category_info['datedim'] == newStart)]

            print('debug print: ', start_date_consumption)
            end_date_consumption = category_info[(category_info['datedim'] == end_date )]
            resupply_quantity = category_info[(category_info['datedim'] == resupply_quantity_date )]
            print('resupply quanity date', resupply_quantity)

            print('debut PRINT BEFORE IF: ', end_date_consumption)
            if end_date_consumption.empty:
                end_date_consumption = category_info[(category_info['datedim'] == category_info.datedim.iloc[-2])]

            whileCount = 1
            dfLen = len(category_info) - len(end_date_consumption)
            print('DF length: ', dfLen)
            
            while resupply_quantity.empty and whileCount < dfLen:
                resupply_quantity = category_info[(category_info['datedim'] == resupply_quantity_date + pd.DateOffset(days=whileCount))]
                whileCount = whileCount + 1


            if not resupply_quantity.empty:
                before_count = end_date_consumption.distinct_id_count_categories.iloc[0] + end_date_consumption.distinct_id_count_categories.iloc[-1]

                print('quantity ', resupply_quantity.distinct_id_count_categories.iloc[0])
                resupply_count = resupply_quantity.distinct_id_count_categories.iloc[0] + resupply_quantity.distinct_id_count_categories.iloc[-1]
                resupply_diff = resupply_count - before_count
                print(' resupply count: ', resupply_count)
                print('Resupply difference', resupply_diff)
            

            print('debut PRINT: ', end_date_consumption)
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
            if category == 'Food-RS':
                calculated_consumption = ((difference_consumption / difference_in_days.days) / 3)
            elif category == 'Food-US':
                calculated_consumption = ((difference_consumption / difference_in_days.days) / 7)
            else:
                calculated_consumption = ((difference_consumption / difference_in_days.days) / 7)

            print('Calculated Consumption Rate: ', calculated_consumption)
            print('Here is the current Rate: ', rates)

            percent_difference = ((calculated_consumption - rates) * 100) / rates 
            print('PERCENT DIFFERENCE IN RATES: ', percent_difference)
            
            
            print('date fordebug: ', start_date_)
            date_string = str(end_date)
            if not resupply_quantity.empty:
                consumption_data = {'date': date_string,'rate': rates, 'calculated_rate': calculated_consumption, 'Percent_Difference': percent_difference, 'Diff_days': difference_in_days.days, 'Diff_Quantity':int(difference_consumption), 'Resupply_Count': int(resupply_diff) }
            else:
                consumption_data = {'date': date_string ,'rate': rates, 'calculated_rate': calculated_consumption, 'Percent_Difference': percent_difference, 'Diff_days': difference_in_days.days, 'Diff_Quantity':int(difference_consumption)}
            json_consumption_data = json.dumps(consumption_data)
            print('percent difference json: ', json_consumption_data)
            return json_consumption_data 


    def calulateResupply(self, resupply_dates):
        crewData = ''
        category = self._category
        resupply_dates = pd.DataFrame(resupply_dates)
        resupply_dates.columns = ['datedim'] + list(resupply_dates.columns[1:])
        print('printing resupply!: ', resupply_dates)

        resupply_dates['New_Column'] = range(len(resupply_dates))
        resupply_dates.set_index('New_Column', inplace=False)
        print(resupply_dates.info)


        print('printing resupply!: ', resupply_dates)
        category_data = self._resupply_dates
        category_data_list = []
        countL = 0
        for index, row in resupply_dates.iterrows(): 
                
            print('Loop COUNT: ', countL)
            countL = countL + 1
            print('IN THE LOOP')
            if len(resupply_dates) > index + 1:
                start_date_str = row['datedim']
                end_date_str = resupply_dates['datedim'][index + 1]
                print('START: ', start_date_str)
                print('END: ', end_date_str)
            else:
                break;
                # # Convert string dates to datetime objects
                # start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                # end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                # Calculate something using your method
            result = self.calculate_something(start_date_str, end_date_str, category, crewData)
            result_json = json.loads(result)
                # Add the results to the list
            category_data_list.append(result_json)

        print("category data list: ", category_data_list)
        frames = {}
        for i, Any in enumerate(category_data_list):
                frames[i] = Any
        print('OUT OF THE LOOP')
                
        # Calculate averages for all categories

        # iterating key value pair
        sumOne = 0
        sumTwo = 0
        sumThree = 0
        sumFour = 0
        sumFive = 0
        print('items: ', frames.items())
        for key in frames.keys():
            print(key, frames[key])
            newFrame = frames[key]

            for innerKey in newFrame.keys():
                print(innerKey, newFrame[innerKey])
                if innerKey == 'calculated_rate':
                    sumOne = sumOne + newFrame[innerKey]
                if innerKey == 'Percent_Difference':
                    sumTwo = sumTwo + newFrame[innerKey]
                if innerKey == 'Diff_days':
                    sumThree = sumThree + newFrame[innerKey]
                if innerKey == 'Diff_Quantity':
                    sumFour = sumFour + newFrame[innerKey]
                if innerKey == 'Resupply_Count':
                    sumFive = sumFive + newFrame[innerKey]
        print('sum one : ', sumOne)
        print('sum two : ', sumTwo)
        print('sum three : ', sumThree)
        print('sum four: ', sumFour )
        print('sum Five: ', sumFive )

        rate_average = sumOne / len(frames)
        print('average_rate: ', rate_average)
        diff_average = sumTwo / len(frames)
        days_average = sumThree / len(frames)
        quantity_average = sumFour / len(frames)
        resupply_average = sumFive / len(frames)


        # Create a dictionary with the averages
        averages_dict = {
            'Category': self._category,
            'RATE_AVERAGE': rate_average,
            'RATE_DIFF_AVERAGE': diff_average,
            'DAYS_BETWEEN_RESUPPLY_AVERAGE': days_average,
            'USAGE_AVERAGE': quantity_average,
            'RESUPPLY_AVERAGE': resupply_average
        }
        # Convert the dictionary to a JSON string
        averages_json = json.dumps(averages_dict)
        
        index = [0]
        
        df = pd.DataFrame(averages_dict, index=index)
        self.load_resupply_data(df)
        # Print the JSON string
        print(df)
    
        newDF = pd.DataFrame(category_data_list)
        print('new df :', newDF)
        dfList_json = newDF.to_json(orient='table')
        return averages_json, dfList_json
    

    def get_category_data(self):
        df = self._category_data
        return(df)
    
    def get_resupply_dates(self):
        df = self._resupply_dates
        return(df)
    
    def get_resupply_data(self):
        df = self._resupply_data
        return(df)
    
    def find_resupply_dates(self, df):
        
        #capture first date from from inventory dataframe
        startDate = df['datedim'][0]
        #get resupply vehicle dock dates
        flights = self.flights
        #Create list starting with first date
        dateList = [startDate]
        print('flights :', flights)
        #loop through inventory dataframe and flight data frame and compare dates
        for i, row in df.iterrows():
            resupply = ''
            #Check for date that has an increase in quantity
            if row['distinct_id_count_categories'] < (df['distinct_id_count_categories'][i + 1]):
                #loop through flight dates
                for j, flight_row in flights.iterrows():
                    category_date = row['datedim']

                    print('debug print: ', category_date)
                    flight_date = flight_row['datedim']
                    #get difference in days of flight date and inventory date
                    difference_in_days = (flight_date) - (category_date)

                    # see if flight is within 7 days of increase                  
                    if difference_in_days.days <= 7 and difference_in_days.days >= -7:
                        print('flight: ', flight_date)
                        print(row['datedim'])   
                        print(df['datedim'][i + 1])
                        print(row['distinct_id_count_categories'])
                        print(df['distinct_id_count_categories'][i + 1])
                        print('difference in days: ', difference_in_days.days)
                        #set resupply as new date
                        resupply = row['datedim']
                        print('resupply date: ', resupply)
                        #creat dummy list and add resupply
                        dummyList = [resupply]
                        break;
            print('length: ', len(df), 'iteration: ', i + 1)
            #Check if resupply is empty
            if resupply != '' :
                #add dummy list to date list
                dateList = dateList + dummyList
            if (len(df) - 1) > i + 1:
                continue;
            else : 
                break;
        #print(resupply)
        print(dateList)
        return (dateList)
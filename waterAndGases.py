import pandas as pd
import json


class waterAndGases:

    def __init__(self, category):
        self._category_data = {}
        self._RSWater_data = {}  # Private attribute
        self._USWater_data = {}  # Private attribute
        self._Gas_data = {}  # Private attribute
        self.flights = {}
        self._resupply_dates = {}
        self._category = category
        self._resupply_data = {}

    def load_flights_data(self, df):
        self.flights = df

    def load_category_data(self, df):
        self._category_data = df

    def load_resupply_data(self, df):
        self._resupply_data = df

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
        start_date_consumption = USWater_info[(
            USWater_info['datedim'] == start_date)]

        if start_date_consumption.empty:
            start_date_consumption = USWater_info[(
                USWater_info['datedim'] == newStart)]

        end_date_consumption = USWater_info[(
            USWater_info['datedim'] == end_date)]
        if end_date_consumption.empty:
            end_date_consumption = USWater_info[(
                USWater_info['datedim'] == USWater_info.datedim.iloc[-1])]
        difference_consumption = start_date_consumption.corrected_potableL.iloc[
            0] - end_date_consumption.corrected_potableL.iloc[-1]
        difference_consumption_technical = start_date_consumption.corrected_technicalL.iloc[
            0] - end_date_consumption.corrected_technicalL.iloc[-1]
        print('DATES:', start_date_consumption, end_date_consumption)
        print('DIFFERENCE between dates: ', difference_consumption)
        ratesPot = 2.844
        ratesTech = 11.5

        difference_in_days = (
            end_date_consumption.datedim.iloc[-1]) - (start_date_consumption.datedim.iloc[0])
        print('Difference in Days: ', (end_date_consumption.datedim.iloc[-1]), ' : ', (
            start_date_consumption.datedim.iloc[0]), ' : ', difference_in_days.days, ' Days')
        calculated_consumption = (
            (difference_consumption / difference_in_days.days) / 4)
        calculated_consumption_tech = (
            ((difference_consumption_technical + (10.435 * difference_in_days.days)) / difference_in_days.days))
        print('Calculated Consumption Rate: ', calculated_consumption)
        print('Here is the current Rate: ', ratesPot)
        print('Calculated Consumption Rate Tech: ', calculated_consumption_tech)
        print('Here is the current Rate: ', ratesTech)
        percent_difference = (
            (calculated_consumption - ratesPot) * 100) / ratesPot
        percent_difference_tech = (
            (calculated_consumption_tech - ratesTech) * 100) / ratesTech

        print('PERCENT DIFFERENCE IN RATES: ', percent_difference)
        print('PERCENT DIFFERENCE IN RATESTECH: ', percent_difference_tech)
        date_string = str(end_date)
        consumption_data = {'date': date_string, 'rate': ratesPot, 'calculated_rate': calculated_consumption, 'Percent_Difference': percent_difference,
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
        resupply_quantity_date = end_date + pd.DateOffset(days=7)
        print('start: ', start_date, ' end: ', end_date,
              ' resupply: ', resupply_quantity_date)

        # Filter based on date range
        newStart = RSWater_info.datedim.iloc[0]
        start_date_consumption = RSWater_info[(
            RSWater_info['datedim'] == start_date)]

        if start_date_consumption.empty:
            print('end date empty')
            start_date_consumption = RSWater_info[(
                RSWater_info['datedim'] == newStart)]

        end_date_consumption = RSWater_info[(
            RSWater_info['datedim'] == end_date)]

        if end_date_consumption.empty:
            print('end date empty')
            end_date_consumption = RSWater_info[(
                RSWater_info['datedim'] == RSWater_info.datedim.iloc[-2])]

        resupply_quantity = RSWater_info[(
            RSWater_info['datedim'] == resupply_quantity_date)]

        if resupply_quantity.empty:
            print('resupply  empty')
            resupply_quantity = RSWater_info[(
                RSWater_info['datedim'] == RSWater_info.datedim.iloc[-1])]

        print('start: ', start_date_consumption, 'End: ',
              end_date_consumption, ' resupply: ', resupply_quantity)

        whileCount = 7
        dfLen = len(RSWater_info) - len(end_date_consumption)
        print('DF length: ', dfLen)

        while resupply_quantity.empty and whileCount < dfLen:
            resupply_quantity = RSWater_info[(
                RSWater_info['datedim'] == resupply_quantity_date + pd.DateOffset(days=whileCount))]
            whileCount = whileCount + 7

        if not resupply_quantity.empty:
            before_count_pot = end_date_consumption.remaining_potableL.iloc[0]
            print('Before count: ', before_count_pot)
            print('quantity potable ',
                  resupply_quantity.remaining_potableL.iloc[0])
            resupply_count_pot = resupply_quantity.remaining_potableL.iloc[0]
            resupply_diff_pot = resupply_count_pot - before_count_pot
            print(' resupply count potable: ', resupply_count_pot)
            print('Resupply difference potable', resupply_diff_pot)

            before_count_tech = end_date_consumption.technicalL.iloc[0]

            print('quantity tech ', resupply_quantity.technicalL.iloc[0])
            resupply_count_tech = resupply_quantity.technicalL.iloc[0]
            resupply_diff_tech = resupply_count_tech - before_count_tech
            print(' resupply count tech : ', resupply_count_tech)
            print('Resupply difference tech', resupply_diff_tech)

            before_count_rod = end_date_consumption.rodnik_potableL.iloc[0]

            print('quantity rod ', resupply_quantity.rodnik_potableL.iloc[0])
            resupply_count_rod = resupply_quantity.rodnik_potableL.iloc[0]
            resupply_diff_rod = resupply_count_rod - before_count_rod
            print(' resupply count rod: ', resupply_count_rod)
            print('Resupply difference rod', resupply_diff_rod)

        difference_consumption = start_date_consumption.remaining_potableL.iloc[
            0] - end_date_consumption.remaining_potableL.iloc[0]
        difference_consumption_technical = start_date_consumption.technicalL.iloc[
            0] - end_date_consumption.technicalL.iloc[0]
        difference_consumption_rod = start_date_consumption.rodnik_potableL.iloc[
            0] - end_date_consumption.rodnik_potableL.iloc[0]

        print('DATES: ', start_date_consumption, end_date_consumption)
        print('DIFFERENCE between dates: ', difference_consumption)
        ratesPot = 2.5
        ratesTech = 11.5

        difference_in_days = (
            end_date_consumption.datedim.iloc[-1]) - (start_date_consumption.datedim.iloc[0])
        print('Difference in Days: ', (end_date_consumption.datedim.iloc[-1]), ' : ', (
            start_date_consumption.datedim.iloc[0]), ' : ', difference_in_days.days, ' Days')
        calculated_consumption = (
            ((difference_consumption + (2.68 * difference_in_days.days)) / difference_in_days.days) / 3)
        calculated_consumption_tech = (
            ((difference_consumption_technical + (10.435 * difference_in_days.days)) / difference_in_days.days))
        print('Calculated Consumption Rate: ', calculated_consumption)
        print('Here is the current Rate: ', ratesPot)
        print('Calculated Consumption Rate Tech: ', calculated_consumption_tech)
        print('Here is the current Rate: ', ratesTech)
        percent_difference = (
            (calculated_consumption - ratesPot) * 100) / ratesPot
        percent_difference_tech = (
            (calculated_consumption_tech - ratesTech) * 100) / ratesTech

        print('PERCENT DIFFERENCE IN RATES: ', percent_difference)
        print('PERCENT DIFFERENCE IN RATESTECH: ', percent_difference_tech)
        date_string = str(end_date)

        consumption_data = {'date': date_string, 'rate': ratesPot, 'calculated_rate': calculated_consumption, 'Percent_Difference': percent_difference,
                            'rateTech': ratesTech, 'calculated_rate_tech': calculated_consumption_tech, 'Percent_DifferenceTech': percent_difference_tech,
                            'Usage_Pot': difference_consumption, 'Usage_Tech': difference_consumption_technical, 'Usage_Rod': difference_consumption_rod,
                            'Resupply_Pot': resupply_diff_pot, 'Resupply_Tech': resupply_diff_tech, 'Resupply_Rod': resupply_diff_rod, 'Diff_in_days': difference_in_days.days}

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
        RSWater_info = RSWater_info[(RSWater_info['datedim'] >= start_date) & (
            RSWater_info['datedim'] <= end_date)]

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
        USWater_info = USWater_info[(USWater_info['datedim'] >= start_date) & (
            USWater_info['datedim'] <= end_date)]

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
        Gas_info = Gas_info[(Gas_info['datedim'] >= start_date)
                            & (Gas_info['datedim'] <= end_date)]

        # Add print statements to display the results
        print("Flights Info:")
        print(Gas_info)
        return Gas_info

    def get_resupply_dates(self):
        df = self._resupply_dates
        return (df)

    def find_resupply_datesRS(self, df):

        # capture first date from from inventory dataframe
        startDate = df['datedim'][0]
        # get resupply vehicle dock dates
        flights = self.flights
        # Create list starting with first date
        print('dataframe: ', df)
        dateList = [startDate]
        print('flights :', flights)
        # loop through inventory dataframe and flight data frame and compare dates
        for i, row in df.iterrows():
            resupply = ''
            # Check for date that has an increase in quantity
            if row['rodnik_potableL'] < (df['rodnik_potableL'][i + 1]):
                # loop through flight dates
                for j, flight_row in flights.iterrows():
                    category_date = row['datedim']
                    print('debug print: ', category_date)
                    flight_date = flight_row['datedim']
                    # get difference in days of flight date and inventory date
                    difference_in_days = (flight_date) - (category_date)
                    # see if flight is within 7 days of increase
                    if difference_in_days.days <= 7 and difference_in_days.days >= -7:
                        print('flight: ', flight_date)
                        print(row['datedim'])
                        print(df['datedim'][i + 1])
                        print(row['rodnik_potableL'])
                        print(df['rodnik_potableL'][i + 1])
                        print('difference in days: ', difference_in_days.days)
                        # set resupply as new date
                        resupply = row['datedim']
                        print('resupply date: ', resupply)
                        # creat dummy list and add resupply
                        dummyList = [resupply]
                        break
            print('length: ', len(df), 'iteration: ', i + 1)
            # Check if resupply is empty
            if resupply != '':
                # add dummy list to date list
                dateList = dateList + dummyList
            if (len(df) - 1) > i + 1:
                continue
            else:
                break
        # print(resupply)
        print(dateList)
        return (dateList)

    def find_resupply_datesUS(self, df):

        # capture first date from from inventory dataframe
        startDate = df['datedim'][0]
        # get resupply vehicle dock dates
        flights = self.flights
        # Create list starting with first date
        print('dataframe: ', df)
        dateList = [startDate]
        print('flights :', flights)
        # loop through inventory dataframe and flight data frame and compare dates
        for i, row in df.iterrows():
            resupply = ''
            # Check for date that has an increase in quantity
            if row['corrected_potableL'] < (df['corrected_potableL'][i + 1]):
                # loop through flight dates
                for j, flight_row in flights.iterrows():
                    category_date = row['datedim']
                    print('debug print: ', category_date)
                    flight_date = flight_row['datedim']
                    # get difference in days of flight date and inventory date
                    difference_in_days = (flight_date) - (category_date)
                    # see if flight is within 7 days of increase
                    if difference_in_days.days <= 7 and difference_in_days.days >= -7:
                        print('flight: ', flight_date)
                        print(row['datedim'])
                        print(df['datedim'][i + 1])
                        print(row['corrected_potableL'])
                        print(df['corrected_potableL'][i + 1])
                        print('difference in days: ', difference_in_days.days)
                        # set resupply as new date
                        resupply = row['datedim']
                        print('resupply date: ', resupply)
                        # creat dummy list and add resupply
                        dummyList = [resupply]
                        break
            print('length: ', len(df), 'iteration: ', i + 1)
            # Check if resupply is empty
            if resupply != '':
                # add dummy list to date list
                dateList = dateList + dummyList
            if (len(df) - 1) > i + 1:
                continue
            else:
                break
        # print(resupply)
        print(dateList)
        return (dateList)

    def find_resupply_datesGAS(self, df):

        # capture first date from from inventory dataframe
        startDate = df['datedim'][0]
        # get resupply vehicle dock dates
        flights = self.flights
        # Create list starting with first date
        print('dataframe: ', df)
        dateList = [startDate]
        print('flights :', flights)
        # loop through inventory dataframe and flight data frame and compare dates
        for i, row in df.iterrows():
            resupply = ''
            # Check for date that has an increase in quantity
            if row['adjusted_O2kg'] < (df['adjusted_O2kg'][i + 1]):
                # loop through flight dates
                for j, flight_row in flights.iterrows():
                    category_date = row['datedim']
                    print('debug print: ', category_date)
                    flight_date = flight_row['datedim']
                    # get difference in days of flight date and inventory date
                    difference_in_days = (flight_date) - (category_date)
                    # see if flight is within 7 days of increase
                    if difference_in_days.days <= 7 and difference_in_days.days >= -7:
                        print('flight: ', flight_date)
                        print(row['datedim'])
                        print(df['datedim'][i + 1])
                        print(row['adjusted_O2kg'])
                        print(df['adjusted_O2kg'][i + 1])
                        print('difference in days: ', difference_in_days.days)
                        # set resupply as new date
                        resupply = row['datedim']
                        print('resupply date: ', resupply)
                        # creat dummy list and add resupply
                        dummyList = [resupply]
                        break
            print('length: ', len(df), 'iteration: ', i + 1)
            # Check if resupply is empty
            if resupply != '':
                # add dummy list to date list
                dateList = dateList + dummyList
            if (len(df) - 1) > i + 1:
                continue
            else:
                break
        # print(resupply)
        print(dateList)
        return (dateList)

    def calulateResupplyRS(self, resupply_dates):
        category = self._category
        resupply_dates = pd.DataFrame(resupply_dates)
        resupply_dates.columns = ['datedim'] + list(resupply_dates.columns[1:])
        print('printing resupply!: ', resupply_dates)

        resupply_dates['New_Column'] = range(len(resupply_dates))
        resupply_dates.set_index('New_Column', inplace=False)
        print(resupply_dates.info)

        print('printing resupply!: ', resupply_dates)
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
                break
                # # Convert string dates to datetime objects
                # start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                # end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

            result = self.calculate_RS_water(start_date_str, end_date_str)
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
        sumSix = 0
        sumSeven = 0
        sumEight = 0
        sumNine = 0
        sumTen = 0
        sumEleven = 0
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
                if innerKey == 'calculated_rate_tech':
                    sumThree = sumThree + newFrame[innerKey]
                if innerKey == 'Percent_DifferenceTech':
                    sumFour = sumFour + newFrame[innerKey]
                if innerKey == 'Usage_Pot':
                    sumFive = sumFive + newFrame[innerKey]
                if innerKey == 'Usage_Tech':
                    sumSix = sumSix + newFrame[innerKey]
                if innerKey == 'Usage_Rod':
                    sumEleven = sumEleven + newFrame[innerKey]
                if innerKey == 'Resupply_Pot':
                    sumSeven = sumSeven + newFrame[innerKey]
                if innerKey == 'Resupply_Tech':
                    sumEight = sumEight + newFrame[innerKey]
                if innerKey == 'Resupply_Rod':
                    sumNine = sumNine + newFrame[innerKey]
                if innerKey == 'Diff_in_days':
                    sumTen = sumTen + newFrame[innerKey]
        print('sum one : ', sumOne)
        print('sum two : ', sumTwo)
        print('sum three : ', sumThree)
        print('sum four: ', sumFour)
        print('sum Five: ', sumFive)
        print('sum Six: ', sumSix)
        print('sum Eleven: ', sumEleven)
        print('sum Seven: ', sumSeven)
        print('sum Eight: ', sumEight)
        print('sum Eight: ', sumNine)
        print('sum Eight: ', sumTen)

        rate_average = sumOne / len(frames)
        print('average_rate: ', rate_average)
        diff_average = sumTwo / len(frames)
        rateTechAvg = sumThree / len(frames)
        diff_average_tech = sumFour / len(frames)
        usage_pot = sumFive / len(frames)
        usage_tech = sumSix / len(frames)
        usage_rod = sumEleven / len(frames)
        resupply_p = sumSeven / len(frames)
        resupply_t = sumEight / len(frames)
        resupply_r = sumNine / len(frames)
        diff_days = sumTen / len(frames)

        # Create a dictionary with the averages
        averages_dict = {
            'Category': self._category,
            'RATE_AVERAGE_POT': rate_average,
            'RATE_DIFF_AVERAGE_POT': diff_average,
            'RATE_AVERAGE_TECH': rateTechAvg,
            'RATE_DIFF_AVERAGE_TECH': diff_average_tech,
            'USAGE_AVERAGE_POT': usage_pot,
            'USAGE_AVERAGE_TECH': usage_tech,
            'USAGE_AVERAGE_ROD': usage_rod,
            'RESUPPLY_AVERAGE_POT': resupply_p,
            'RESUPPLY_AVERAGE_TECH': resupply_t,
            'RESUPPLY_AVERAGE_ROD': resupply_r,
            'DAYS_BETWEEN_RESUPPLY_AVERAGE': diff_days

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

    def calulateResupplyUS(self, resupply_dates):
        category = self._category
        resupply_dates = pd.DataFrame(resupply_dates)
        resupply_dates.columns = ['datedim'] + list(resupply_dates.columns[1:])
        print('printing resupply!: ', resupply_dates)

        resupply_dates['New_Column'] = range(len(resupply_dates))
        resupply_dates.set_index('New_Column', inplace=False)
        print(resupply_dates.info)

        print('printing resupply!: ', resupply_dates)
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
                break
                # # Convert string dates to datetime objects
                # start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                # end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

            result = self.calculate_US_water(start_date_str, end_date_str)
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
        sumSix = 0
        sumSeven = 0
        sumEight = 0
        sumTen = 0
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
                if innerKey == 'calculated_rate_tech':
                    sumThree = sumThree + newFrame[innerKey]
                if innerKey == 'Percent_DifferenceTech':
                    sumFour = sumFour + newFrame[innerKey]
                if innerKey == 'Usage_Pot':
                    sumFive = sumFive + newFrame[innerKey]
                if innerKey == 'Usage_Tech':
                    sumSix = sumSix + newFrame[innerKey]
                if innerKey == 'Resupply_Pot':
                    sumSeven = sumSeven + newFrame[innerKey]
                if innerKey == 'Resupply_Tech':
                    sumEight = sumEight + newFrame[innerKey]
                if innerKey == 'Diff_in_days':
                    sumTen = sumTen + newFrame[innerKey]
        print('sum one : ', sumOne)
        print('sum two : ', sumTwo)
        print('sum three : ', sumThree)
        print('sum four: ', sumFour)
        print('sum Five: ', sumFive)
        print('sum Six: ', sumSix)
        print('sum Seven: ', sumSeven)
        print('sum Eight: ', sumEight)
        print('sum Eight: ', sumTen)

        rate_average = sumOne / len(frames)
        print('average_rate: ', rate_average)
        diff_average = sumTwo / len(frames)
        rateTechAvg = sumThree / len(frames)
        diff_average_tech = sumFour / len(frames)
        usage_pot = sumFive / len(frames)
        usage_tech = sumSix / len(frames)
        resupply_p = sumSeven / len(frames)
        resupply_t = sumEight / len(frames)
        diff_days = sumTen / len(frames)

        # Create a dictionary with the averages
        averages_dict = {
            'Category': self._category,
            'RATE_AVERAGE_POT': rate_average,
            'RATE_DIFF_AVERAGE_POT': diff_average,
            'RATE_AVERAGE_TECH': rateTechAvg,
            'RATE_DIFF_AVERAGE_TECH': diff_average_tech,
            'USAGE_AVERAGE_POT': usage_pot,
            'USAGE_AVERAGE_TECH': usage_tech,
            'RESUPPLY_AVERAGE_POT': resupply_p,
            'RESUPPLY_AVERAGE_TECH': resupply_t,
            'DAYS_BETWEEN_RESUPPLY_AVERAGE': diff_days

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

    def calulateResupplyGas(self, resupply_dates):
        category = self._category
        resupply_dates = pd.DataFrame(resupply_dates)
        resupply_dates.columns = ['datedim'] + list(resupply_dates.columns[1:])
        print('printing resupply!: ', resupply_dates)

        resupply_dates['New_Column'] = range(len(resupply_dates))
        resupply_dates.set_index('New_Column', inplace=False)
        print(resupply_dates.info)

        print('printing resupply!: ', resupply_dates)
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
                break
                # # Convert string dates to datetime objects
                # start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                # end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

            result = self.calculate_US_water(start_date_str, end_date_str)
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
        sumSix = 0
        sumSeven = 0
        sumEight = 0
        sumTen = 0
        print('items: ', frames.items())
        for key in frames.keys():
            print(key, frames[key])
            newFrame = frames[key]

            for innerKey in newFrame.keys():
                print(innerKey, newFrame[innerKey])
                if innerKey == 'calculated_rate_for_O2':
                    sumOne = sumOne + newFrame[innerKey]
                if innerKey == 'Percent_Difference_O2':
                    sumTwo = sumTwo + newFrame[innerKey]
                if innerKey == 'calculated_rate_tech_N2':
                    sumThree = sumThree + newFrame[innerKey]
                if innerKey == 'Percent_DifferenceTech_N2':
                    sumFour = sumFour + newFrame[innerKey]
                if innerKey == 'Usage_Pot_N2':
                    sumFive = sumFive + newFrame[innerKey]
                if innerKey == 'Usage_Tech_N2':
                    sumSix = sumSix + newFrame[innerKey]
                if innerKey == 'Resupply_Pot_O2':
                    sumSeven = sumSeven + newFrame[innerKey]
                if innerKey == 'Resupply_Tech_N2':
                    sumEight = sumEight + newFrame[innerKey]
                if innerKey == 'Diff_in_days':
                    sumTen = sumTen + newFrame[innerKey]
        print('sum one : ', sumOne)
        print('sum two : ', sumTwo)
        print('sum three : ', sumThree)
        print('sum four: ', sumFour)
        print('sum Five: ', sumFive)
        print('sum Six: ', sumSix)
        print('sum Seven: ', sumSeven)
        print('sum Eight: ', sumEight)
        print('sum Eight: ', sumTen)

        rate_average_O2 = sumOne / len(frames)
        print('average_rate: ', rate_average_O2)
        diff_average_O2 = sumTwo / len(frames)
        rateTechAvg_N2 = sumThree / len(frames)
        diff_average_tech_N2 = sumFour / len(frames)
        usage_pot_N2 = sumFive / len(frames)
        usage_tech_N2 = sumSix / len(frames)
        resupply_pot_O2 = sumSeven / len(frames)
        resupply_tech_N2 = sumEight / len(frames)
        diff_days = sumTen / len(frames)

        # Create a dictionary with the averages
        averages_dict = {
            'Category': self._category,
            'RATE_AVERAGE_POT': rate_average_O2,
            'RATE_DIFF_AVERAGE_POT': diff_average_O2,
            'RATE_AVERAGE_TECH': rateTechAvg_N2,
            'RATE_DIFF_AVERAGE_TECH': diff_average_tech_N2,
            'USAGE_AVERAGE_POT': usage_pot_N2,
            'USAGE_AVERAGE_TECH': usage_tech_N2,
            'RESUPPLY_AVERAGE_POT': resupply_pot_O2,
            'RESUPPLY_AVERAGE_TECH': resupply_tech_N2,
            'DAYS_BETWEEN_RESUPPLY_AVERAGE': diff_days

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

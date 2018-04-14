import MySQLdb, json
import time, os, shutil, datetime, sys
import pandas as pd
import numpy as np



class dataAnalytic:

    def __init__(self):
        self.__mysql_host = 'ucdgroup18.ck04mjz0uhn8.us-west-2.rds.amazonaws.com'
        self.__mysql_user = 'root'
        self.__mysql_password = '1234qwer'
        self.__weather_db = 'weather'
        self.__bike_db = 'bike'
        self.__current_path = os.path.dirname(os.path.abspath(__file__))


    def __createInterval(self):
        plots = list(range(24))
        interval = {}
        for i in plots:
            interval[i+1] = [i*3600, (i+1)*3600-1]
        return interval
    
    def __getClock(self, interval, timestamp):
        for key,value in interval.items():
            remainder = int(timestamp/1000 % (3600*24)) * 1000
            if self.__isInInterval(value, remainder):
                return key 

    def __analyzingOnWeather(self, weather):
        """
        Return Value: A dictionary:
       		{weather_name: times}
        """
        weather_analytics = {}
        for key, value in weather.items():
            if value[0] not in weather_analytics.keys():
                weather_analytics[value[0]] = 1
            else:
                weather_analytics[value[0]] += 1
        return weather_analytics

    def __isInInterval(self, duration, mytime):
        return int(duration[0]) <= mytime/1000 <= int(duration[1])

    def getOneDayPerWeekBikeData(self):
        t, oneWeekWeather = self.__getWeatherData()
        interval = self.__createInterval()
        try:
            mydb = MySQLdb.connect(host= self.__mysql_host,
                                   user = self.__mysql_user,
                                   passwd = self.__mysql_password,
                                   db = self.__bike_db)
            cursor = mydb.cursor()
        except Exception as e:
            print(str(e))

        intervalRate = []
        intervalRecord = {}
        cursor.execute('select * from BikeStationHistory')
        row = cursor.fetchone()
        while row is not None:
            stationID = row[0]
            timestamp = int(row[11].strip("'"))
            Available_bike_stands = row[9]
            Bike_stands = row[10]
            for key, value in oneWeekWeather.items():
                if self.__isInInterval(value[1], timestamp):
                    clock = self.__getClock(self.__createInterval(), int(timestamp))
                    weather = value[0]
                    if weather.lower() != 'rain':
                        weather = 'NonRain'
                    else:
                        weather = 'Rain'
                    if clock not in intervalRecord.keys():
                        intervalRecord[clock] = {}
                        intervalRecord[clock]['Rain'] = [0,0]
                        intervalRecord[clock]['NonRain'] = [0,0]
                        intervalRecord[clock][weather] = [int(Available_bike_stands), int(Bike_stands)]
                    else:
                        intervalRecord[clock][weather][0] += int(Available_bike_stands)
                        intervalRecord[clock][weather][1] += int(Bike_stands)
            row = cursor.fetchone()
        for key, value in intervalRecord.items():
            mydict = {'clock': 0,
                      'rate': {}
                     }
                              
            for k, v in value.items():
                mydict['clock'] = str(key) + ":00:00"
                weather = k
                if int(v[0]) == 0:
                    mydict['rate'][weather]=0
                    #intervalRate[key][k] = 0
                else:
                    mydict['rate'][weather]=round(float(v[1])/float(v[0]),2)
                    #intervalRate[key][k] = round(float(v[1])/float(v[0]),2)
            intervalRate.append(mydict)
        mydb.commit()
        cursor.close()

        return intervalRate


    def getOneWeekBikeData(self):
        t, oneWeekWeather = self.__getWeatherData()
        try:
            mydb = MySQLdb.connect(host= self.__mysql_host,
                                   user = self.__mysql_user,
                                   passwd = self.__mysql_password,
                                   db = self.__bike_db)
            cursor = mydb.cursor()
        except Exception as e:
            print(str(e))
        
        w_analytics = self.__analyzingOnWeather(oneWeekWeather)
        cursor.execute('select * from BikeStationHistory')
        row = cursor.fetchone()
        statics = {}
        stations = {}
        BikeStandsAccount = 0
        while row is not None:
            stationID = row[0]
            if stationID not in stations.keys():
                stations[stationID] = int(row[8])
            timestamp= int(row[11].strip("'"))
            for key, value in oneWeekWeather.items():
                if self.__isInInterval(value[1], timestamp):
                    bikeStands = int(row[8])
                    BikeStandsAccount += bikeStands
                    availableBikeStands = int(row[9])
                    weather = value[0]
                    if weather in statics.keys():
                        statics[weather] += availableBikeStands
                    else:
                        statics[weather] = availableBikeStands
            row = cursor.fetchone()
        mydb.commit()
        cursor.close()
        totalBikeStands = 0
        for key, value in stations.items():
            totalBikeStands += value

        staticsRates = {}
        for key in statics.keys():
            interval = float(w_analytics[key])
            staticsRates[key] = float(statics[key])/(interval*3*12*totalBikeStands)
    
        
        return totalBikeStands, staticsRates

    
    def getOneMonthData(self, weather_dict, bike_dict): 
        try:
            mydb = MySQLdb.connect(host= self.__mysql_host,
                                   user = self.__mysql_user,
                                   passwd = self.__mysql_password,
                                   db = self.__bike_db)
            cursor = mydb.cursor()
        except Exception as e:
            print(str(e))

        intervalRate = []
        intervalRecord = {}
        cursor.execute('select * from BikeStationHistory')
        row = cursor.fetchone()
        while row is not None:
            new_row = []
            stationID = row[0]
            timestamp = int(row[11].strip("'"))
            clock = int((timestamp/1000) % (3600*24) / 3600)
            Available_bike_stands = row[9]
            Bike_stands = row[10]
            new_row = [stationID, Available_bike_stands, Bike_stands, clock, timestamp/1000]
            print(new_row)
            break
            row = cursor.fetchone()
        mydb.commit()
        cursor.close()

    def __getWeatherData(self):
        try:
            mydb = MySQLdb.connect(host=self.__mysql_host,
                                   user = self.__mysql_user,
                                   passwd = self.__mysql_password,
                                   db = self.__weather_db)
            cursor = mydb.cursor()
        except Exception as e:
            print(str(e))

        # timestamp
        now = int(time.time())
        # 1 month ago
        monthago = now - 2592000
        # 1 week ago
        weekago = now - 604800

        # define how may days before
        daysBefore = monthago
        # 3 hours interal
        interal = 3600*3

        cursor.execute('select * from WeatherDetails')
        row = cursor.fetchone()
        t = {}
        oneWeekWeather = {}
        while row is not None:
            timestamp= int(row[0].strip("'"))
            end_timestamp = timestamp + interal - 1
            weather_main = row[10].strip("'")
            dateStr = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            t[row[0]] = [dateStr, [timestamp, end_timestamp], weather_main]
            row = cursor.fetchone()
        for key,value in t.items():
            if int(key.strip("'")) >= daysBefore:
                cursor.execute('select Weather_Main from WeatherDetails where Dt=%s', [key])
                row_weather = cursor.fetchone()[0].strip("'")
                oneWeekWeather[int(key.strip("'"))] = [row_weather, t[key][1]]
            #cursor.execute('select * from WeatherDetails where Dt=%s', [key])
            #cursor.execute('update WeatherDetails set Dt_txt=%s where Dt=%s',[t[key], key])

        mydb.commit()
        cursor.close()
        return t, oneWeekWeather

    def writeToJson(self, json_file=None):
        json_stream = json.dumps(self.getOneDayPerWeekBikeData())
        if json_file is None:
            filename = self.__current_path + '/../../../data/Dublin_Chart_6.json'
        else:
            filename = self.__current_path + '/../../../data/' + json_file
        try:
            with open(filename, 'w', encoding='utf8') as f:
                f.write(json_stream)
        except Exception as e:
            print("Warning: Can not open " + filename)
            print(e)
        f.close()

    def createInputData(self):
        '''This will create a simple dictionary for weather and bike'''
        Weather_Main = ['Rain','Clouds','Clear']
        weather_dict = {'Temp': 10,
                        'Humidity': 80,
                        'Weather_Main': 'Rain',
                        'Wind_speed': 20,
                        'Rain3H': 250}
        bike_dict = {'Number':1,
                     'Clock':1}
        return weather_dict, bike_dict
  
    def insertClockToMysql(self):
        '''temperary method'''
        # timestamp
        now = int(time.time())
        # 1 month ago
        monthago = now - 2592000
        # 1 week ago
        weekago = now - 604800
        try:
            mydb = MySQLdb.connect(host= self.__mysql_host,
                                   user = self.__mysql_user,
                                   passwd = self.__mysql_password,
                                   db = self.__bike_db)
            cursor = mydb.cursor()
        except Exception as e:
            print(str(e))

        intervalRate = []
        intervalRecord = {}
        cursor.execute('select * from BikeStationHistory order by Last_update desc')
        row = cursor.fetchone()
        count = 0
        timeDict = {}
        while row is not None:
            timestamp = int(row[11].strip("'"))
            #print(timestamp, weekago*1000)
            if timestamp < weekago*1000:
                row = cursor.fetchone()
                continue
            else:
                clock = int(timestamp/1000 % (3600*24) / 3600)
                timeDict[row[11]] = clock
                #print(count, row[11], clock, weekago*1000)
            #if count >= 10:
            #    break;
            #count = count + 1
            row = cursor.fetchone()
        print(len(timeDict.keys()))
        count = 0
        for key, value in timeDict.items():
            count = count + 1
            #print("key=", key, ",value=", value)
            cursor.execute('UPDATE BikeStationHistory SET Clock = %s WHERE Last_update = %s', (value, key))
            if count % 200 == 0:
                print("Counting: ", count, key)
        mydb.commit()
        cursor.close()


def main():
    myAnalytic = dataAnalytic()
#print(oneWeekWeather)
#print(t)
#w_analytics = analyzingOnWeather(oneWeekWeather)
#print(w_analytics)
    #bikeStands, rates = myAnalytic.getOneWeekBikeData()
    #print(rates, bikeStands)
#dict = myAnalytic.getOneDayPerWeekBikeData()
#print(dict)
    #myAnalytic.writeToJson()

    #weather_dict, bike_dict = myAnalytic.createInputData()
    #myAnalytic.getOneMonthData(weather_dict, bike_dict)
    myAnalytic.insertClockToMysql()


if __name__ == '__main__': 
    main()


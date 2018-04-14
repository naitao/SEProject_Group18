import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb, json
import time, os, shutil, datetime, sys

# Import package for reading csv files 
import pandas as pd

class makeCSV:
    def __init__(self):
        self.__mysql_host = 'ucdgroup18.ck04mjz0uhn8.us-west-2.rds.amazonaws.com'
        self.__mysql_user = 'root'
        self.__mysql_password = '1234qwer'
        self.__weather_db = 'weather'
        self.__bike_db = 'bike'
        self.__current_path = os.path.dirname(os.path.abspath(__file__))

    def writeToBikeCSV(self):
        now = int(time.time())
        #current_time = now % (3600*24)
        now_days = int(now/(3600*24))
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
        cursor.execute('select * from BikeStationHistory order \
                           by Last_update desc limit 50')
        row = cursor.fetchone()
        d = { 'Number':[],
              'Available_bike_stands':[],
              'Bike_stands':[],
              'Clock':[],
              'TimeStamp':[],
              'Date':[],
              'Days':[]}
        df = pd.DataFrame(data=d)
        count=0
        while row is not None:
            stationID = row[0]
            timestamp = int(row[11].strip("'"))
            clock = int((timestamp/1000) % (3600*24) / 3600)
            days = int(timestamp/(1000*3600*24)) - now_days
            dateStr = datetime.datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%d %H:%M:%S')
            Available_bike_stands = row[9]
            Bike_stands = row[8]
            d['Number'] = str(stationID)
            d['Available_bike_stands'] = str(Available_bike_stands)
            d['Bike_stands'] = str(Bike_stands)
            d['Clock'] = str(clock)
            d['Date'] = dateStr
            d['TimeStamp'] = str(int(timestamp/1000))
            d['Days'] = str(days)
            df=df.append(d,ignore_index=True)
            row = cursor.fetchone()
        mydb.commit()
        cursor.close()
        file = self.__current_path + "/../../../data/bikeStation.csv"
        df.to_csv(file,index=False)
        print("Bike CSV writting finished!")

    def writeToWeatherCSV(self):
        try:
            mydb = MySQLdb.connect(host=self. __mysql_host,
                                   user = self.__mysql_user,
                                   passwd = self.__mysql_password,
                                   db = self.__weather_db)
            cursor = mydb.cursor()
        except Exception as e:
            print(str(e))

        now = int(time.time())
        #current_time = now % (3600*24)
        now_days = int(now/(3600*24))
        w_dict = {'Dt':[],
                  'Temp':[],
                  'Humidity':[],
                  'WeatherMain':[],
                  'WindSpeed':[],
                  'Rain3H':[],
                  'Clock':[],
                  'day':[]}
        df2 = pd.DataFrame(data=w_dict)
        cursor.execute('select * from WeatherDetails order by Dt')
        row = cursor.fetchone()
        while row is not None:
            timestamp = int(row[0].strip("'"))
            clock = int(timestamp % (3600*24) / 3600)
            day = int(timestamp/(3600*24)) - now_days
            w_dict = {'Dt':str(row[0].strip("'")),
                      'Temp':row[1],
                      'Humidity':row[7],
                      'WeatherMain':str(row[10].strip("'")),
                      'WindSpeed':row[14],
                      'Rain3H':row[16],
                      'Clock':clock,
                      'day':str(day)}
            df2=df2.append(w_dict,ignore_index=True)
            row = cursor.fetchone()
        mydb.commit()
        cursor.close()
        file = self.__current_path + "/../../../data/weatherDetails.csv"
        df2.to_csv(file,index=False)
        print("Weather CSV writting finished!")

def main():
    my = makeCSV()
    my.writeToBikeCSV()
    my.writeToWeatherCSV()


if __name__ == '__main__':
    main()

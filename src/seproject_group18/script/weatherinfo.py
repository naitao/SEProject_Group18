from urllib.request import urlopen
import os, shutil, datetime, sys
import csv, json
import codecs
import MySQLdb
import time
from seproject_group18.script import dataAnalytic
from threading import Thread

class Weatherinfo(Thread):
    def __init__(self, url):
        Thread.__init__(self)
        self.daemon = True
        self.start()
        self.url = url
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.__mysql_host = 'ucdgroup18.ck04mjz0uhn8.us-west-2.rds.amazonaws.com'
        self.__mysql_db = 'weather'
        self.__mysql_user = 'root'
        self.__mysql_password = '1234qwer'
        self.__json_file = self.current_path + '/../../../data/' + 'Dublin_weather_updated.json'
        self.__csv_file = self.current_path + '/../../../data/' + 'Dublin_weather_updated.csv'
            
    def __call_response(self):
        try:
            response = urlopen(self.url)
        except Exception as e:
            print("Warning: Can not open " + self.url)
            print(str(e))
            response = None
        return response
        
    def to_json(self, json_file=None):
        response = self.__call_response()
        if response is not None:
            if json_file is None:
                filename = self.__json_file
            else:
                filename = self.current_path + '/../../../data/' + json_file
            try:
                f = open(filename, 'wb')
                shutil.copyfileobj(response, f)
            except Exception as e:
                print("Warning: Can not open " + filename)
                print(e)
            f.close()
            self.__json_file = filename
        else:       
            print("Can not save to a json file")

    def to_csv(self, csv_file=None):
        response = self.__call_response()
        
        if csv_file is None:
            filename = self.__csv_file
        else:
            filename = self.current_path + '/../../../data/' + csv_file
        reader = codecs.getreader("utf-8")
        if response is not None:
            #data = list(json.load(reader(response)))
            data = json.load(reader(response))
            csv_keys = ['dt', 'main', 'weather', 'clouds', 'wind', 'rain', 'sys', 'dt_txt']
            with open(filename, 'w', newline='') as csv_stream:
                fieldnames = ['Dt','Temp','Temp_Min','Temp_Max','Pressure', 'Sea_Level', 'Grnd_Level', 'Humidity', 'Temp_Kf',
                    'Weather_Id', 'Weather_Main', 'Weather_Description', 'Weather_Icon',
                    'Clouds_All', 'Wind_Speed', 'Wind_Deg',
                    'Rain_3h',
                    'Sys_Pod',
                    'Dt_txt']
                csv_app = csv.DictWriter(csv_stream, fieldnames=fieldnames)
                csv_app.writeheader()
                for i in range(len(data['list'])):
                    csv_values = []
                    #print(data['list'][i])
                    for key in csv_keys:
                        if key is 'main':
                            csv_values.append(data['list'][i][key]['temp'])
                            csv_values.append(data['list'][i][key]['temp_min'])
                            csv_values.append(data['list'][i][key]['temp_max'])
                            csv_values.append(data['list'][i][key]['pressure'])
                            csv_values.append(data['list'][i][key]['sea_level'])
                            csv_values.append(data['list'][i][key]['grnd_level'])
                            csv_values.append(data['list'][i][key]['humidity'])
                            csv_values.append(data['list'][i][key]['temp_kf'])
                        elif key is 'weather':
                            csv_values.append(data['list'][i][key][0]['id'])
                            csv_values.append(data['list'][i][key][0]['main'])
                            csv_values.append(data['list'][i][key][0]['description'])
                            csv_values.append(data['list'][i][key][0]['icon'])
                        elif key is 'clouds':
                            csv_values.append(data['list'][i][key]['all'])
                        elif key is 'wind':
                            csv_values.append(data['list'][i][key]['speed'])
                            csv_values.append(data['list'][i][key]['deg'])
                        elif key is 'rain':
                            if 'rain' in data['list'][i] and len(data['list'][i][key]) == 1:
                                csv_values.append(data['list'][i][key]['3h'])
                            else:
                                csv_values.append(0)
                        elif key is 'sys':
                            csv_values.append(data['list'][i][key]['pod'])
                        else:
                            csv_values.append(data['list'][i][key])
                    try:
                        csv_app.writerow({'Dt': csv_values[0],
                                         'Temp': csv_values[1],
                                         'Temp_Min': csv_values[2],
                                         'Temp_Max': csv_values[3],
                                         'Pressure': csv_values[4],
                                         'Sea_Level': csv_values[5],
                                         'Grnd_Level': csv_values[6],
                                         'Humidity': csv_values[7],
                                         'Temp_Kf': csv_values[8],
                                         'Weather_Id': csv_values[9],
                                         'Weather_Main': csv_values[10],
                                         'Weather_Description': csv_values[11],
                                         'Weather_Icon': csv_values[12],
                                         'Clouds_All': csv_values[13],
                                         'Wind_Speed': csv_values[14],
                                         'Wind_Deg': csv_values[15],
                                         'Rain_3h': csv_values[16],
                                         'Sys_Pod': csv_values[17],
                                         'Dt_txt': csv_values[18],
                                         })
                    except Exception as e:
                        print("Error: can get csv data: " + filename)
                        print(str(e))
                        break

            self.__csv_file = filename

    def copy_jsonfile(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        source = current_path + "/../../../data/Dublin_weather_updated.json"
        dest = current_path + "/../app/static/Dublin_weather_updated.json"
        os.system("cp {} {}".format(source, dest))

    def import_to_mysql(self, mode = 'update', csv_file=None,
                        mysql_host=None,
                        mysql_db=None,
                        mysql_user=None,
                        mysql_password=None):
        if csv_file is None:
            filename = self.__csv_file
        else:
            filename = self.current_path + '/../../../data/' + csv_file
        
        mysql_host = mysql_host if mysql_host is not None else self.__mysql_host
        mysql_db = mysql_db if mysql_db is not None else self.__mysql_db
        mysql_user = mysql_user if mysql_user is not None else self.__mysql_user
        mysql_password = mysql_password if mysql_password is not None else self.__mysql_password
        try:
            mydb = MySQLdb.connect(host=mysql_host,
                user = mysql_user,
                passwd = mysql_password,
                db = mysql_db)
            cursor = mydb.cursor()
        except Exception as e:
            print(str(e))

        csv_data = csv.reader(open(filename, 'r'))
        for row in csv_data:
            if 'Dt' in row and 'Temp_Max' in row:
                continue
            if mode is 'update':
                row.append(row[0])
                cursor.execute('INSERT INTO WeatherDetails(Dt, Temp, Temp_Min, Temp_Max, \
                    Pressure, Sea_Level, Grnd_Level, Humidity, Temp_Kf, Weather_Id, \
                    Weather_Main, Weather_Description, Weather_Icon, Clouds_All, Wind_Speed, Wind_Dep, Rain_3h, Sys_Pod, Dt_txt)' \
                    'VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s") ON DUPLICATE KEY UPDATE Dt="%s"',
                    [row[0], round(float(row[1]), 2),
                     round(float(row[2]), 2), round(float(row[3]), 2),
                     round(float(row[4]), 2), round(float(row[5]), 2),
                     round(float(row[6]), 2), round(float(row[7]), 2), round(float(row[8]), 2),
                     int(row[9]), row[10], row[11], row[12], int(row[13]),
                     round(float(row[14]), 2), round(float(row[15]), 2), round(float(row[16]), 2),
                     row[17], row[18], row[0]])
            elif mode is 'init':
                cursor.execute('CREATE TABLE IF NOT EXISTS WeatherDetails( \
                    Dt VARCHAR(255) PRIMARY KEY, \
                    Temp FLOAT(10, 2), \
                    Temp_Min FLOAT(10, 2), \
                    Temp_Max FLOAT(10, 2), \
                    Pressure FLOAT(10, 2), \
                    Sea_Level FLOAT(10, 2), \
                    Grnd_Level FLOAT(10, 2), \
                    Humidity FLOAT(10, 2), \
                    Temp_Kf FLOAT(10, 2), \
                    Weather_Id INT(10), \
                    Weather_Main VARCHAR(45), \
                    Weather_Description VARCHAR(45), \
                    Weather_Icon VARCHAR(45), \
                    Clouds_All INT(10), \
                    Wind_Speed FLOAT(10, 2), \
                    Wind_Dep FLOAT(10, 2), \
                    Rain_3h FLOAT(10, 2), \
                    Sys_Pod VARCHAR(4), \
                    Dt_txt VARCHAR(255))')
                break
                    
        #close the connection to the database.
        mydb.commit()
        cursor.close()



'''
# WEATHER INFORMATION
# Current weather info (2 ways)
#weather_url = 'http://api.openweathermap.org/data/2.5/weather?id=2964574&appid=3641377121f997a81e12f28ba9831df1'
#weather_url = 'http://api.openweathermap.org/data/2.5/weather?q=Dublin&appid=3641377121f997a81e12f28ba9831df1'

# 5 Days weather info (Detailed weather information)
weather_url = 'http://api.openweathermap.org/data/2.5/forecast/?id=7778677&mode=json&units=metric&APPID=19b104f014c41d11939f615df3a80edf'
myweather = Weatherinfo(weather_url)
myweather.to_json()
myweather.to_csv()

# Only for the first time for creating table
#myweather.import_to_mysql(mode='init')
# Regulare updating DB with APIs
myweather.import_to_mysql()
'''

def main():
    weather_url = 'http://api.openweathermap.org/data/2.5/forecast/?id=7778677&mode=json&units=metric&APPID=19b104f014c41d11939f615df3a80edf'
    myweather = Weatherinfo(weather_url)
    myAnalytic = dataAnalytic.dataAnalytic()
    myweather.to_csv()
    while True:
        myweather.to_json()
        myweather.to_csv()
        myweather.import_to_mysql()
        print("Weather information from APIs updated on DB (12 hours)")
        myweather.copy_jsonfile()
        print("Weather information JSON is updated onto flask static folder (12 hours)")
        myAnalytic.writeToJson()       
        print("Bike information analyzed data updated on JSON file")

        # Update weather information onto RDS every 12 hours
        time.sleep(3600*12)

if __name__ == '__main__':
    main() 

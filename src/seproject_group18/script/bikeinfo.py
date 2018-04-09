from urllib.request import urlopen
import os, shutil, datetime, sys
import csv, json
import codecs
import MySQLdb
import time
from threading import Thread

class Bikeinfo(Thread):
    def __init__(self, url):
        Thread.__init__(self)
        self.daemon = True
        self.start()
        self.url = url
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.__mysql_host = 'ucdgroup18.ck04mjz0uhn8.us-west-2.rds.amazonaws.com'
        self.__mysql_db = 'bike'
        self.__mysql_user = 'root'
        self.__mysql_password = '1234qwer'
        self.__json_file = self.current_path + '/../../../data/' + 'Dublin_bike_updated.json'
        self.__csv_file = self.current_path + '/../../../data/' + 'Dublin_bike_updated.csv'
            
    def __call_response(self):
        try:
            response = urlopen(self.url)
        except Exception as e:
            print("Warning: Can not open " + self.url)
            print(str(e))
            response = None
        return response
        
    def toMute(self):  #抑制输出
        self.nulObj = open(os.devnull, 'w')
        sys.stdout = self.nulObj

    def toCons(self):  #标准输出重定向至控制台
        sys.stdout = self.savedStdout #sys.__stdout__

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
            data = list(json.load(reader(response)))
            csv_keys = ['number', 'name', 'address', 'position',
                'banking', 'bonus',
                'status', 'bike_stands', 'available_bike_stands', 'available_bikes',
                'last_update']
            with open(filename, 'w', newline='') as csv_stream:
                fieldnames = ['Number','Name','Address','Latitude','Longitude',
                    'Banking', 'Bonus', 'Status', 'Bike_stands',
                    'Available_bike_stands', 'Available_bikes',
                     'Last_update']
                csv_app = csv.DictWriter(csv_stream, fieldnames=fieldnames)
                csv_app.writeheader()
                for i in range(len(data)):
                    csv_values = []
                    for key in csv_keys:
                        if key is 'position':
                            csv_values.append(data[i][key]['lat'])
                            csv_values.append(data[i][key]['lng'])
                        else:
                            csv_values.append(data[i][key])
                    #print(csv_values, "\n")
                    try:
                        csv_app.writerow({'Number': csv_values[0],
                                         'Name': csv_values[1],
                                         'Address': csv_values[2],
                                         'Latitude': csv_values[3],
                                         'Longitude': csv_values[4],
                                         'Banking': csv_values[5],
                                         'Bonus': csv_values[6],
                                         'Status': csv_values[7],
                                         'Bike_stands': csv_values[8],
                                         'Available_bike_stands': csv_values[9],
                                         'Available_bikes': csv_values[10],
                                         'Last_update': csv_values[11]})
                    except Exception as e:
                        print("Error: can get csv data: " + filename)
                        print(str(e))
                        break

            self.__csv_file = filename

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
            if 'Name' in row and 'Address' in row:
                continue
            if mode is 'update':
                row.append(row[0])
                cursor.execute('INSERT INTO BikeStation(Number, \
                    Name, Address, Latitude, Longitude, Banking, Bonus, Status, Bike_stands, Available_bike_stands, Available_bikes, Last_update)' \
                    'VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s") ON DUPLICATE KEY UPDATE Number="%s"',
                    [int(row[0]), row[1], row[2], float(row[3]), float(row[4]), row[5], row[6], row[7], int(row[8]), int(row[9]), int(row[10]), row[11], int(row[0])])
            elif mode is 'incr':
                cursor.execute('INSERT INTO BikeStationHistory(Number, \
                    Name, Address, Latitude, Longitude, Banking, Bonus, Status, Bike_stands, Available_bike_stands, Available_bikes, Last_update)' \
                    'VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")',
                    [int(row[0]), row[1], row[2], float(row[3]), float(row[4]), row[5], row[6], row[7], int(row[8]), int(row[9]), int(row[10]), row[11]])
            elif mode is 'init':
                cursor.execute('CREATE TABLE IF NOT EXISTS BikeStationHistory( \
                    Number INT(10) PRIMARY KEY, \
                    Name VARCHAR(45), \
                    Address VARCHAR(45), \
                    Latitude FLOAT(10,8), \
                    Longitude FLOAT(10,8), \
                    Banking VARCHAR(10), \
                    Bonus VARCHAR(10), \
                    Status VARCHAR(10), \
                    Bike_stands INT(4), \
                    Available_bike_stands INT(4), \
                    Available_bikes INT(4), \
                    Last_update VARCHAR(255))')
                break
                    
        #close the connection to the database.
        mydb.commit()
        cursor.close()

'''
# Bike info
bike_url = 'https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=7ecf9f5fd2eae31adbf96d743cae7c173f850c11'
mybike = Bikeinfo(bike_url)
#mybike.to_json()
mybike.to_csv()
# Only for the first time for creating table
#mybike.import_to_mysql(mode='init')
mybike.import_to_mysql(mode='incr')

'''

def main():
    bike_url = 'https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=7ecf9f5fd2eae31adbf96d743cae7c173f850c11'
    mybike = Bikeinfo(bike_url)
    while True:
        mybike.to_csv()
        mybike.import_to_mysql()
        mybike.import_to_mysql(mode='incr')
        print("Bike information from APIs updated on DB (5mins)")

        # update bike information onto RDS every 5 mins
        time.sleep(300)

if __name__ == '__main__':
    main() 

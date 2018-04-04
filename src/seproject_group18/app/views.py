from flask import Flask, redirect, render_template, session, url_for
from flaskext.mysql import MySQL
app = Flask(__name__, static_url_path = "")
#from seproject_group18.app import app
app.config['MYSQL_DATABASE_HOST'] = 'ucdgroup18.ck04mjz0uhn8.us-west-2.rds.amazonaws.com'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1234qwer'
app.config['MYSQL_DATABASE_DB'] = 'bike'
mysql = MySQL(app)

@app.route('/') 
def index(): 
        returnDict = {} 
        returnDict['user'] = 'COMP30670'    # Feel free to put your name here! 
        returnDict['title'] = 'Home' 
        return render_template("index.html", **returnDict)

@app.route('/weather/') 
def weather(): 
        return render_template("forecaster_updated.html")

@app.route('/weatherjson/') 
def weatherjsion(): 
        return app.send_static_file("Dublin_weather_updated.json")
@app.route('/bike/') 
def bike(): 
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute('''SELECT Address FROM BikeStation''')
        rv = cur.fetchall()
        returnDict = {}
        returnDict['user'] = rv[0]    # Feel free to put your name here! 
        returnDict['title'] = rv[1]
        returnDict['sysinfo'] = rv[2]
        return render_template("bike.html", **returnDict)

@app.route('/weather/icons/<name>') 
def icon(name): 
        return render_template("{}".format(name))

@app.route('/bike5/') 
def bike5():
        return render_template("bike5.html")
@app.route('/bike5json/')
def bike5json():
        return app.send_static_file("Dublin_bike_updated.json")
@app.route('/charts.js/')
def chartsjs():
        return app.send_static_file("Charts.js")
@app.route('/charts.min.js/')
def chartsminjs():
        return app.send_static_file("Chart.min.js")
@app.route('/charts.bundle.js/')
def chartsbundlejs():
        return app.send_static_file("Chart.bundle.js")
@app.route('/charts.bundle.min.js/')
def chartsbundleminjs():
        return app.send_static_file("Chart.bundle.min.js")

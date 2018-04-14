from flask import Flask, redirect, render_template, session, url_for, request
from flaskext.mysql import MySQL
app = Flask(__name__, static_url_path = "")
from seproject_group18.script import dataAnalytic

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

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
        #myAnalytic = dataAnalytic.dataAnalytic()
        #bikeStands,rate = myAnalytic.getOneWeekBikeData()
        returnDict = {}
        returnDict['title'] = "COMP30430"    # Feel free to put your name here! 
        
        returnDict['rate'], returnDict['bikeStands'] = "A", "B"
        return render_template("bike.html", **returnDict)
@app.route('/bikeReview/') 
def bikeAnalytics(): 
        return render_template("bikeReview.html")

@app.route('/weather/icons/<name>') 
def icon(name): 
        return render_template("{}".format(name))

@app.route('/bike5/') 
def bike5():
        return render_template("bike5.html")
@app.route('/bike5json/')
def bike5json():
        return app.send_static_file("Dublin_bike_updated.json")
@app.route('/chart6.js/')
def chart5():
        return app.send_static_file("chart6.js")
@app.route('/charts.js/')
def chartsjs():
        return app.send_static_file("Chart.js")
@app.route('/charts.min.js/')
def chartsminjs():
        return app.send_static_file("Chart.min.js")
@app.route('/charts.bundle.js/')
def chartsbundlejs():
        return app.send_static_file("Chart.bundle.js")
@app.route('/charts.bundle.min.js/')
def chartsbundleminjs():
        return app.send_static_file("Chart.bundle.min.js")


@app.route('/station_chart6/')
def chart6():
        return app.send_static_file("Dublin_Chart_6.json")
@app.route('/station_chart7/')
def chart7():
        return app.send_static_file("Dublin_Chart_7.json")


@app.route('/test/')
def test():
    return render_template('test.html')

@app.route('/analyze', methods=['GET', 'POST'])
def server():
    if request.method == 'POST':
        returnDict = {} 
        # Then get the data from the form
        returnDict['temp'] = request.form['Temp']
        returnDict['humidity'] = request.form['Humi']
        returnDict['weather'] = request.form['Weat']
        returnDict['rain3h'] = request.form['Rain']
        returnDict['windspeed'] = request.form['Wind']

        # Generate just a boring response
        #return 'The credentials for %s are %s and %s' % (temp, humidity, weather) 
        return render_template('bikeReview.html', **returnDict)

    # Otherwise this was a normal GET request
    else:   
        return render_template('index.html')

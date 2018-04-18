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

'''
@app.route('/') 
def index(): 
        returnDict = {} 
        returnDict['user'] = 'COMP30670'    # Feel free to put your name here! 
        returnDict['title'] = 'Home' 
        return render_template("index.html", **returnDict)
'''

@app.route('/weather/') 
def weather(): 
        return render_template("forecaster_updated.html")

@app.route('/weatherjson/') 
def weatherjsion(): 
        return app.send_static_file("Dublin_weather_updated.json")
'''
@app.route('/bike/') 
def bike(): 
        #myAnalytic = dataAnalytic.dataAnalytic()
        #bikeStands,rate = myAnalytic.getOneWeekBikeData()
        returnDict = {}
        returnDict['title'] = "COMP30430"    # Feel free to put your name here! 
        
        returnDict['rate'], returnDict['bikeStands'] = "A", "B"
        return render_template("bike.html", **returnDict)
'''
@app.route('/bikeReview/') 
def bikeReview(): 
        return render_template("bikeReview.html")

@app.route('/weather/icons/<name>') 
def icon(name): 
        return render_template("{}".format(name))

@app.route('/') 
def index():
        return render_template("index.html")
@app.route('/bike5json/')
def bike5json():
        return app.send_static_file("Dublin_bike_updated.json")

@app.route('/markers.js/')
def markers():
        return app.send_static_file("markers.js")
@app.route('/charts.js/')
def chartsjs():
        return app.send_static_file("Chart.js")
@app.route('/chart1.js/')
def chart1():
        return app.send_static_file("chart1.js")
@app.route('/chart2.js/')
def chart2():
        return app.send_static_file("chart2.js")
@app.route('/chart6.js/')
def chart6():
        return app.send_static_file("chart6.js")
@app.route('/weather.js/')
def wheather():
        return app.send_static_file("weather.js")
@app.route('/bikeCss.css/')
def bikeCss():
        return app.send_static_file("bikeCss.css")
@app.route('/bootstrap.min.css/')
def bootstrapmincss():
        return app.send_static_file("bootstrap.min.css")
@app.route('/font-awesome.css/')
def fontawesomecss():
        return app.send_static_file("font-awesome.css")
@app.route('/style.css/')
def stylecss():
        return app.send_static_file("style.css")
@app.route('/modernizr.custom.js/')
def modernizrcustomjs():
        return app.send_static_file("modernizr.custom.js")
@app.route('/jquery-1.11.2.min.js/')
def jquery1112minjs():
        return app.send_static_file("jquery-1.11.2.min.js")
@app.route('/wow.min.js/')
def wowminjs():
        return app.send_static_file("wow.min.js")
@app.route('/owl-carousel.js/')
def owlcarouseljs():
        return app.send_static_file("owl-carousel.js")
@app.route('/nivo-lightbox.min.js/')
def nivolightboxminjs():
        return app.send_static_file("nivo-lightbox.min.js")
@app.route('/smoothscroll.js/')
def smoothscrolljs():
        return app.send_static_file("smoothscroll.js")
@app.route('/bootstrap.min.js/')
def bootstrapminjs():
        return app.send_static_file("bootstrap.min.js")
@app.route('/classie.js/')
def classiejs():
        return app.send_static_file("classie.js")
@app.route('/script.js/')
def cscriptjs():
        return app.send_static_file("script.js")
@app.route('/bike.jpg/')
def bikejpg():
        return app.send_static_file("bike.jpg")




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
def stationChart6():
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
        #'{{ number }}', '{{ location }}', '{{ usedBikes}}', '{{ bikeStands }}
        # Then get the data from the form
        if len(request.form['Number']) == 0 or \
            len(request.form['Temp']) == 0 or len(request.form['Humi']) == 0 or \
                len(request.form['Weat']) == 0 or len(request.form['Wind']) == 0:
                    return render_template('bikeReview.html')
        number = int(request.form['Number'])
        temp = float(request.form['Temp'])
        humidity = int(request.form['Humi'])
        weather = request.form['Weat']
        windspeed = float(request.form['Wind'])

        myAnalytic = dataAnalytic.dataAnalytic()
        returnDict['location'] = myAnalytic.getBikeStations()[int(number)]
        returnDict['number'] = number
        returnDict['usedBikes'], returnDict['bikeStands'] = \
            myAnalytic.getPredictionOnStation(temp=temp,humidity=humidity,weather=weather,\
                windSpeed=windspeed,stationNumber=number)

        # Generate just a boring response
        return render_template('bikeReview.html', **returnDict)

    # Otherwise this was a normal GET request
    else:   
        return render_template('bike5.html')

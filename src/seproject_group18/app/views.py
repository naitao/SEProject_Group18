from flask import render_template 
from seproject_group18.app import app
from systeminfo import sysinfo
@app.route('/') 
def index(): 
        returnDict = {} 
        returnDict['user'] = 'COMP30670'    # Feel free to put your name here! 
        returnDict['title'] = 'Home' 
        returnDict['sysinfo'] = sysinfo.get_platform_info()
        return render_template("index.html", **returnDict)

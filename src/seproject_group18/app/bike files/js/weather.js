// Anna code
    // Global variables here
    //
    var weatherInfo  = "</br><table border = 1 >"; // global variable which correspond to main weather info 
    
    // Global variable which sets current date/time for filter.
    var currDate     = new Date("2018-03-12 05:00:00");  // new Date();
    var dispInt      = 8; // means 24hrs display interval. can be up to 40.
    
    //
    //  Function that loads JSON fie with main weather info
    //
    function loadJSON()
    {
        var xmlhttp = new XMLHttpRequest();
        var url = "Dublin_weather_updated.json";

         xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {

            //Parse the JSON data to a JavaScript variable. 
            window.parsedObj = JSON.parse(xmlhttp.responseText); 
            
            // This function is defined below and deals with the JSON data parsed from the file. 
            //   NOTE: for test "coord":{"lat":53.3551,"lon":-6.2493},
            displayWeather(parsedObj, dispInt, currDate, 53.3551, -6.2493); 
        }
    };

    xmlhttp.open("GET", url, true);
    xmlhttp.send();
    }
        
        
    // 
    // Here we display main weather info:
    //  obj - loaded JSON object
    //  displayInterval  (=8 by default for 24hrs) - how many weather records we want to display
    //  currDateTime      - curent date/time for weather filter
    //  currLat, currLon  - lattitude/longitude - for location filter
    //
    function displayWeather(obj, displayInterval, currDateTime, currLat, currLong) 
    { 
        var daysArray    = obj.list;
        var quotes       = "\"";
        var NumberOfDays = Math.min(displayInterval, daysArray.length);
        var currDateTimeUTC = Math.floor(currDateTime.getTime() / 1000) 
        var startOffset = 0;
        
        //console.log("number of days :", NumberOfDays);
        //console.log("date/UTC timestamp  :", currDateTime, currDateTimeUTC);
             
        for (var i=0; i< daysArray.length; i++) {
          if (daysArray[i].dt >= currDateTimeUTC) {
              break; }
            startOffset++;
        }
            
        // new data, something to display
        if (startOffset < daysArray.length)
        {
            if ( obj.city.coord.lat == currLat &&
                  obj.city.coord.lon == currLong )
            {

                // Main weather info - table header
                weatherInfo += "<tr>";    
                for (var i=0; i < NumberOfDays; i++) {  
                   weatherInfo += "<td>" + daysArray[i+startOffset].dt_txt + "</td>";

                }

                weatherInfo +="</tr><tr>";
                for (var i=0; i < NumberOfDays; i++) {
                  weatherInfo += "<td><img src=/../" + daysArray[i+startOffset].weather[0].icon + ".png width=64 height=64></img></td>"; 
                }

                weatherInfo +="</tr><tr>";
                for (var i=0; i < NumberOfDays; i++)  {
                   weatherInfo += "<td>" + daysArray[i+startOffset].weather[0].description + "</td>";
                }

                weatherInfo +="</tr><tr>";
                for (var i=0; i < NumberOfDays; i++) {   
                     weatherInfo += "<td>"+daysArray[i+startOffset].main.temp + "°C</td>";
                }

                weatherInfo +="</tr><tr>";

                for (var i=0; i < NumberOfDays; i++) {
                    weatherInfo += "<td>" + daysArray[i+startOffset].main.humidity + "%</td>";
                }
                weatherInfo +="</tr><tr>";

                for (var i=0; i < NumberOfDays; i++) {
                    weatherInfo +="<td>" + daysArray[i+startOffset].wind.speed + "km/h</td>"
                }
                weatherInfo +="</tr>";
            }
            else
            {
                weatherInfo +="<b>Undefined location lat:"+currLat+", lon:"+currLong+".</b>";    
            }
        }
        else // no new weather data..
        {
            weatherInfo +="<b>No current weather update</b>";
        }
        
        // Close the table element.
        weatherInfo += "</table>"; 
      
        // Finally, we constructed string. Lets assign it to actual HTML property
        document.getElementById("weatherId").innerHTML = weatherInfo;
    }
     //
     // This function triggers when user clicks submit button.
     //
    function changeSelection()
     {
        loadJSON();
        weatherInfo  = "</br><table border = 0 >";
    } 
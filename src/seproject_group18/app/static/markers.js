        //var myValue = ['{{ number }}', '{{ location }}', '{{ usedBikes}}', '{{ bikeStands }}'];
        function initMap() {
        var map = new google.maps.Map(document.getElementById('map'), {
          center: new google.maps.LatLng(53.3481, -6.2593),
          zoom: 14
        });
   
            
            var xmlhttp = new XMLHttpRequest();
            //var url = "Dublin_bike_updated.json";
            //var url = "/bike5json/";
            var url = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=7ecf9f5fd2eae31adbf96d743cae7c173f850c11";
            xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
        
        //Parse the JSON data to a JavaScript variable. 
                    var parsedObj = JSON.parse(xmlhttp.responseText);    
        // This function is defined below and deals with the JSON data parsed from the file.
                displayInfo(parsedObj);
    		}
	};
	xmlhttp.open("GET", url, true);
	xmlhttp.send();
        function displayInfo(obj){
            for(var i=0;i<obj.length;i++){
                var infoWindow = new google.maps.InfoWindow;
                var number = obj[i].number;
                var name = obj[i].name;
                var address = obj[i].address;
                var available_bikes = obj[i].available_bikes;
                var available_bike_stands = obj[i].available_bike_stands;
                var bike_stands = obj[i].bike_stands;
                var banking = obj[i].banking;
                var bonus = obj[i].bonus;
                var myStatus = obj[i].status;
                var lat = obj[i].position.lat;
                var lng = obj[i].position.lng;
                var position = new google.maps.LatLng(parseFloat(lat),parseFloat(lng));

                var infowincontent = document.createElement('div');
              
                var strong = document.createElement('strong');
                strong.textContent = "Station no. " + number
                infowincontent.appendChild(strong);
                infowincontent.appendChild(document.createElement('br'));

                var text1 = document.createElement('text');
                text1.textContent = "Full address: " + address
                infowincontent.appendChild(text1);
                infowincontent.appendChild(document.createElement('br'));
                
                var text2 = document.createElement('text');
                text2.textContent = "Available bikes: " + available_bikes
                infowincontent.appendChild(text2);
                infowincontent.appendChild(document.createElement('br'));
                
                var text3 = document.createElement('text');
                text3.textContent = "Free stands: " + available_bike_stands
                infowincontent.appendChild(text3);
                infowincontent.appendChild(document.createElement('br'));
                
                var text4 = document.createElement('text');
                text4.textContent = "Total capacity: " + bike_stands
                infowincontent.appendChild(text4);
                infowincontent.appendChild(document.createElement('br'));
            
                var text5 = document.createElement('text');
                text5.textContent = "Banking: " + banking
                infowincontent.appendChild(text5);

                var text6 = document.createElement('text');
                text6.textContent = "Bonus: " + bonus;
                infowincontent.appendChild(text6);
                infowincontent.appendChild(document.createElement('br'));

                var text7 = document.createElement('text');
                text7.textContent = "Status: " + myStatus;
                infowincontent.appendChild(text7);
              
               
                var marker = new google.maps.Marker({map: map,
                                                     position: position,
                                                     label: number.toString(),
                                                     infowincontent: infowincontent});
                google.maps.event.addListener(marker, 'click', function() {
                    infoWindow.setContent(this.infowincontent);
                    infoWindow.open(map, this);
                });

            }
          }
        }
        
         

//<script async defer
 //   src="https://maps.googleapis.com/maps/api/js?key=AIzaSyD-JwqLtuvHobOKXLxrkkn4I5XcgbcB8AE&callback=initMap">
//</script>

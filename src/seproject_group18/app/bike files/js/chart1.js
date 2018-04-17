$.getJSON("Dublin_bike_updated.json", function (json) {
    var labels = json.map(function(item) {
      return item.name;
    });
    var availableBikes = json.map(function(item){
      return item.available_bikes;
    });
        // Find the top 10 stations;
    var isSwap;
    var temp1;
    var temp2;
    // sort
    for(var i=0; i< availableBikes.length;i++){
        isSwap = false;
        for (var j = 0; j< availableBikes.length - 1 - i;j++){
            if(availableBikes[j]<availableBikes[j+1]){
                isSwap = true;
                temp1 = availableBikes[j+1];
                availableBikes[j+1] = availableBikes[j];
                availableBikes[j] = temp1;
                temp2 = labels[j+1];
                labels[j+1] = labels[j];
                labels[j] = temp2;
            }
        }
        
    }
        
    var NewBikes = new Array(10);
    var NewLabels = new Array(10);
    for (var k = 0; k<10;k++){
        NewBikes[k] = availableBikes[k];
        NewLabels[k] = labels[k];
    }
 
    var data = {
      labels: NewLabels,
      datasets: [
      {
        label: "available bikes",
        fillColor: "rgba(10,87,105,0.5)",
        strokeColor: "rgba(151,187,205,0.8)",
        highlightFill: "rgba(151,187,205,0.75)",
        highlightStroke: "rgba(151,187,205,1)",
        data: NewBikes
      }
      ]
    };
    var options = {
        legend: { display: false },
        title: {
            display: true,
            text: 'Find the best 10 stations to take bikes '
        }
    };
    var ctx = document.getElementById("myChart1").getContext("2d");
    ctx.canvas.width = 1400;
    ctx.canvas.height = 300;

    var myChart1 = new Chart(ctx).Bar(data, {barShowStroke: true});
  });
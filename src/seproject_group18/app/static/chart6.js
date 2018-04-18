$.getJSON("Dublin_Chart_6.json", function (json) {
  // Chart 6
  // will generate array with ['Monday', 'Tuesday', 'Wednesday']
  var labels = json.map(function(item) {
    return item.clock;
  });
  var Rate = json.map(function(item){
    return item.rate;
  });
  var RainRate = new Array(24);
  var nonRainRate = new Array(24);
  for (var i=0; i<Rate.length; i++){
      	RainRate[i] = Rate[i].Rain;
      	nonRainRate[i] = Rate[i].NonRain;
  }
  var data = {
    labels: labels,
    datasets: [
    {
      label: "Rain",
      fillColor: "rgb(87, 160, 255)",
      strokeColor: "rgba(220,220,220,0.8)",
      highlightFill: "rgba(220,220,220,0.75)",
      highlightStroke: "rgba(220,220,220,1)",
      data: RainRate
    },
    {
      label: "NonRain",
      fillColor: "rgb(133, 140, 140)",
      highlightFill: "rgba(151,187,205,0.8)",
      highlightFill: "rgba(151,187,205,0.75)",
      highlightStroke: "rgba(151,187,205,1)",
      data: nonRainRate
    }
    ]
  };
  var options = {
      legend: { display: false },
      title: {
          display: true,
          text: 'One week bike usage calculations'
      }
  }
  var ctx = document.getElementById("myChart").getContext("2d");
  ctx.canvas.width = 1100;
  ctx.canvas.height = 300;

  var myChart = new Chart(ctx).Bar(data, {barShowStroke: false});
});

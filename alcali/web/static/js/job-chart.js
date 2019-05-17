/*
  jobChart.

 */
let ctx = document.getElementById('jobChart').getContext('2d');
let jobChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: [],
    datasets: [{
      lineTension: 0.1,
      pointRadius: 1,
      data: [0], // fake data before update(needed for plugin).
      fill: false,
      colorStart: 'rgba(0, 173, 238, 1.0)',
      colorEnd: 'rgba(231, 18, 143, 1.0)'
    }, {
      lineTension: 0.1,
      pointRadius: 1,
      data: [0],
      fill: false,
      colorStart: 'rgba(255, 255, 255, 1.0)',
      colorEnd: 'rgba(255, 0, 0, 1.0)'
    }]
  },
  options: {
    linearGradientLine: true,
    legend: {
      display: false
    },
    scales: {
      xAxes: [{
        gridLines: {
          display: true
        }
      }],
      yAxes: [{
        gridLines: {
          display: true
        },
        ticks: {
          autoSkip: true,
          beginAtZero: true,
          maxTicksLimit: 6
        }
      }]
    },
    responsive: true
  }
});

// Update graph for the given period.
function updateGraph() {
  let period = document.getElementById('period').value;
  let filter = document.getElementById('filter').value;
  // Ajax call.
  $.ajax({
    type: 'POST',
    data: {
      'period': period,
      'filter': filter,
      csrfmiddlewaretoken: token
    },

    // handle a successful response
    success: function (ret) {
      jobChart.data.labels = ret.labels;
      jobChart.data.datasets[0].data = ret.series[0];
      jobChart.data.datasets[1].data = ret.series[1];
      jobChart.update();
    },

    // handle a non-successful response
    error: function(xhr, errmsg, err) {
      // TODO: change for graph
      $('#results').html('<div class=\'alert-box alert radius\' data-alert>Oops! We have encountered an error: ' + errmsg +
        ' <a href=\'#\' class=\'close\'>&times;</a></div>'); // add the error to the dom
      console.log(xhr.status + ': ' + xhr.responseText); // provide a bit more info about the error to the console
    }
  });
}

// Init on page load.
updateGraph();

function realtimeChart() {
  let lastEl = jobChart.data.datasets[0].data.length - 1;
  jobChart.data.datasets[0].data[lastEl] += 1;
  jobChart.update();
}
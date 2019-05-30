let highstateConformity = document.getElementById('highstateConformity');
highstateConformity.addEventListener('click', (ev) => {
  let target = document.getElementById('target').value;
  $.ajax({
    type: 'POST',
    data: {
      target: target,
      csrfmiddlewaretoken: token,
      cron: cronField.cron("value")
    },

    // handle a successful response
    success: function (ret) {
      if (ret.result === 'updated') {
        showNotification(
          'bg-black',
          'Minion field created',
          'bottom',
          'center'
        );
      }
    },

    // handle a non-successful response
    error: function (xhr, errmsg, err) {
      // TODO: change for graph
      $('#results').html('<div class=\'alert-box alert radius\' data-alert>Oops! We have encountered an error: ' + errmsg +
        ' <a href=\'#\' class=\'close\'>&times;</a></div>'); // add the error to the dom
      console.log(xhr.status + ': ' + xhr.responseText); // provide a bit more info about the error to the console
    }
  });
});

$('.flatpickr').flatpickr({
  enableTime: true,
  noCalendar: true,
  dateFormat: 'H:i',
  time_24hr: true
});
let cronField = $('#cronSelector').cron({
  initial: '0 0 * * *',
  customValues: {
    'half hour': '*/30 * * * *'
  }
});

$(document).ready(function() {
  $.ajax({
    type: 'POST',
    "data": {
      csrfmiddlewaretoken: token,
      action: "list"
    },
    success: function(result) {
      console.log(result);
      result.columns.forEach((column, index) => {
        if (index >= conformityColDef.length) {
          conformityColDef.push({
            "title": column,
            "name": column
          })
        } else {
          conformityColDef[index].title = column;
        }
      });
      conformityColDef.push(
        { name: "Action",
          render: function(data, type, row, meta) {
            if (type === "display") {
              data = '<a href="/conformity/' + row[0] + '/" class="btn btn-primary btn-sm waves-effect" role="button">DETAIL</a>\n'+
                '<a href="/run?tgt=' + row[1] + '&fun='+ row[2] +'" class="btn bg-blue-grey btn-sm waves-effect" role="button">RERUN</a>';
            }
            return data;
          },
          className: "text-center"
        }
      );
      $(".js-basic-example").DataTable({
        data: result.data,
        columns: conformityColDef
      });
    }
  });
});

let conformityColDef = [
  { name: "Minion id",
    render: function (data, type, row, meta) {
      if (type === "display") {
        data = '<a href="/minions/' + data + '/">' + data + '</a>';
      }
      return data;
    }
  },
  { name: "Highstate Conformity",
    render: function(data, type, row, meta) {
      if (type === "display") {
        if (data === true) {
          data = '<span class="label bg-green">CONFORM</span>';
        } else if (data === false) {
          data = '<span class="label bg-red">CONFLICT</span>';
        } else  if (data === null) {
          data = '<span class="label bg-blue-grey">UNKNOWN</span>';
        }
      }
      return data;
    },
    className: "text-center"
  },
  { name: "Succeeded",
    render: function (data, type, row, meta) {
      if (type === "display") {
        if (data !== null) {
          data = '<span class="label bg-green">' + data + '</span>';
        }
      }
      return data;
    },
    className: "text-center"
  },
  { name: "Unchanged",
    render: function (data, type, row, meta) {
      if (type === "display") {
        if (data === null || data === 0) {
          data = null
        } else {
          data = '<span class="label bg-orange">' + data + '</span>';
        }
      }
      return data;
    },
    className: "text-center"
  },
  { name: "Failed",
    render: function (data, type, row, meta) {
      if (type === "display") {
        if (data === null || data === 0) {
          data = null
        } else {
          data = '<span class="label bg-red">' + data + '</span>';
        }
      }
      return data;
    },
    className: "text-center"
  },
];

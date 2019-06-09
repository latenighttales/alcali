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

//Exportable table

$(document).ready(function() {
  $.ajax({
    type: 'POST',
    data: {
      csrfmiddlewaretoken: token,
    },
    success: function(result) {
      // create column definition.
      let schedColDef = [];
      let enabledCol = 0;
      result.columns.forEach((column, index) => {
        if (column === 'enabled') {enabledCol = index};
        schedColDef.push({
          "title": column,
          // Render bool as badge.
          render: function(data, type, row, meta) {
            if (type === "display") {
              if (typeof data === "boolean") {
                if (data) {
                  data = '<span class="label bg-green">'+data+'</span>';
                } else {
                  data = '<span class="label bg-red">'+data+'</span>';
                }
              }
            }
            return data;
          },
        })
      });
      // add minion link to first column.
      schedColDef[0]['render'] = function(data, type, row, meta) {
        if (type === "display") {
          data = '<a href="/minions/' + data + '/">' + data + '</a>';
        }
        return data;
      };
      // Add action button.
      schedColDef.push({
        "title": "Action",
        data: null,
        render: function(data, type, row, meta) {
          if (type === "display") {
            data = '<button class="btn btn-primary btn-sm waves-effect" data-toggle="modal" data-target="#defaultModal">COPY</button>\n';
            // Enable btn.
            if (row[enabledCol]) {
              data += '<button class="btn btn-warning btn-sm waves-effect" onclick="manageSchedule(\'disable_job\', \''+row[2]+'\', \''+row[0]+'\')">DISABLE</button>\n';
            } else {
              data += '<button class="btn btn-warning btn-sm waves-effect" onclick="manageSchedule(\'enable_job\', \''+row[2]+'\', \''+row[0]+'\')">ENABLE</button>\n';
            }
            data += '<button class="btn btn-danger btn-sm waves-effect" onclick="manageSchedule(\'delete\', \''+row[2]+'\', \''+row[0]+'\')">DELETE</button>\n';
          }
          return data;
        },
        className: "text-center"
      });
      $(".js-exportable").DataTable({
        order: [[0, "desc"]],
        dom: "<'row'<'col-sm-6'l><'col-sm-6'f>>" +
          "<'row'<'col-sm-12'tr>>" +
          "<'row'<'col-sm-2'i><'col-sm-3 pull-left'B><'col-sm-7'p>>",
        responsive: true,
        buttons: [
          "copy", "csv", "excel", "print"
        ],
        data: result.data,
        columns: schedColDef
      });
    }
  });
});

function manageSchedule(action, name, minion = null) {
  if (action === 'copy') {

  }
  $.ajax({
    type: 'POST',
    data: {
      action: action,
      minion: minion,
      name: name,
      csrfmiddlewaretoken: token
    },

    // handle a successful response
    success: function() {
      showNotification(
        'bg-black',
        '<b>action: </b>' + action + ' on ' + minion + ': ' + name + ' done',
        'bottom',
        'center'
      )
    },

    // handle a non-successful response
    error: function(xhr, errmsg, err) {
      console.log(xhr.status + ': ' + xhr.responseText); // provide a bit more info about the error to the console
    }
  });

}
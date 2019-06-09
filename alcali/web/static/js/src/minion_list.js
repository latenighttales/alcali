
let minionColDef = [
  { name: "Minion Id",
    render: function(data, type, row, meta) {
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
        } else if (data === null) {
          data = '<span class="label bg-blue-grey">UNKNOWN</span>';
        } else {
          data = '<span class="label label-danger">CONFLICT</span>';
        }
      }
      return data;
    },
    className: "text-center"
  },
  { name: "Fqdn" },
  { name: "OS" },
  { name: "OS Version" },
  { name: "Kernel" },
  { name: "Last Job" },
  { name: "Last Highstate",
    render: function(data, type, row, meta) {
      if (type === "display") {
        // TODO: use Locale locale..
        if (data !== null) {
          data = new Date(data).toLocaleString('en-GB');
        }
      }
      return data;
    }
  },
  { name: "Action",
    render: function(data, type, row, meta) {
      if (type === "display") {
        data = '<button class="btn btn-primary btn-sm waves-effect" onclick="manageMinion(\'refresh\',\''+row[0]+'\')">REFRESH</button>\n';
        data += '<a href="/run?tgt='+row[0]+'" class="btn btn-sm bg-blue-grey waves-effect" role="button">RUN JOB</a>\n';
        data += '<button class="btn btn-danger btn-sm waves-effect" id="'+ row[0] +'" data-toggle="modal" data-target="#defaultModal">DELETE</button>\n';
      }
      return data;
    },
    className: "text-center"
  }
];



let minionTable;
function createMinionTable() {
  minionTable = $('.js-exportable').DataTable({
    "order": [[0, "desc"]],
    dom: "<'row'<'col-sm-6'l><'col-sm-6'f>>" +
      "<'row'<'col-sm-12'tr>>" +
      "<'row'<'col-sm-2'i><'col-sm-3 pull-left'B><'col-sm-7'p>>",
    responsive: true,
    buttons: [
      "copy", "csv", "excel", "print"
    ],
    "ajax": {
      "url": "/minions",
      "type": "POST",
      "data": {
        csrfmiddlewaretoken: token
      },
    },
    "columns": minionColDef
  });
}
createMinionTable();

// Delete minion modal.
$('#defaultModal').on('show.bs.modal', function(e) {
  let minion = e.relatedTarget.id;
  console.log(minion);
  let deleteBtn = document.getElementById('deleteMinion');
  deleteBtn.addEventListener('click', () => {
    manageMinion('delete', minion);
    $('#closeModal').trigger('click');
  });
});

/*
  Manage minions db.
  action: 'delete' TODO: restrain actions.
  minion: target. 'all' will target all minions.
 */
function manageMinion(action, minion) {
    showNotification('bg-black', '<b>action: </b>' + action + ' on ' + minion + ' submitted', 'bottom', 'center');
  // Ajax call.
  $.ajax({
    type: "POST",
    url: '/minions',
    data: {
      csrfmiddlewaretoken: token,
      minion: minion,
      action: action
    },

    // handle a successful response
    success: function (ret) {
      minionTable.ajax.reload();
      showNotification('bg-black', '<b>action: </b>' + action + ' on ' + minion + ' done', 'bottom', 'center');
    },

    // handle a non-successful response
    error: function (xhr, errmsg, err) {
      $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
        " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
      console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
  });
}


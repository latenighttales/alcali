// Keys column definition.
let keysColDef = [
  { name: "Minion id",
    render: function(data, type, row, meta) {
      if (type === "display") {
        if (row[1] === "accepted") {
          data = '<a href="/minions/' + data + '/">' + data + '</a>';
        }
      }
      return data;
    }
  },
  { name: "Key status",
    render: function(data, type, row, meta) {
      if (type === "display") {
        if (data === "accepted") {
          data = '<span class="label bg-green">' + data.toUpperCase() + '</span>';
        } else if (data === "rejected") {
          data = '<span class="label bg-red">' + data.toUpperCase() + '</span>';
        } else if (data === "unaccepted") {
          data = '<span class="label bg-primary">' + data.toUpperCase() + '</span>';
        }
      }
      return data;
    },
    className: "text-center"
  },
  { name: "Public key" },
  { name: "Action",
    render: function(data, type, row, meta) {
      if (type === "display") {
        console.log(row[1]);
        if (row[1] === "accepted") {
          data = '<button class="btn btn-warning btn-sm waves-effect" onclick="manageKey(\'delete\', \''+row[0]+'\')">DELETE</button>\n';
          data += '<button class="btn btn-danger btn-sm waves-effect" onclick="manageKey(\'reject\', \''+row[0]+'\')">REJECT</button>\n';
        } else if (row[1] === "rejected") {
          data = '<button class="btn btn-success btn-sm waves-effect" onclick="manageKey(\'accept\', \''+row[0]+'\')">ACCEPT</button>\n';
          data += '<button class="btn btn-danger btn-sm waves-effect" onclick="manageKey(\'reject\', \''+row[0]+'\')">REJECT</button>\n';
        } else  if (row[1] === "unaccepted") {
          data = '<button class="btn btn-success btn-sm waves-effect" onclick="manageKey(\'accept\', \''+row[0]+'\')">ACCEPT</button>\n';
        }
      }
      return data;
    },
    className: "text-center"
  }
];

function manageKey(action, target) {
  showNotification(
    "bg-black",
    "<b>action: </b>" + action + " on " + target + " submitted",
    "bottom",
    "center"
  );
  $.ajax({
    url: '/run',
    type: 'POST',
    data: {
      action: action,
      target: target,
      csrfmiddlewaretoken: token
    },

    // handle a successful response
    success: function(ret) {
      if (ret.hasOwnProperty('error')) {
        showNotification(
          "bg-red",
          "<b>error: </b>" + ret.error,
          "bottom",
          "center"
        );
      } else {
        showNotification(
          "bg-black",
          "<b>action: </b>" + action + " on " + target + " done",
          "bottom",
          "center"
        );
      }
      tableKeys.ajax.reload();
    },

    // handle a non-successful response
    error: function(xhr, errmsg, err) {
      console.log(errmsg);
      console.log(xhr.status + ': ' + xhr.responseText); // provide a bit more info about the error to the console
    }
  });
}

let tableKeys;
function createKeysTable() {
  tableKeys = $(".js-basic-example").DataTable({
    responsive: true,
    ajax: {
      url: "/keys",
      type: "POST",
      data: {
        csrfmiddlewaretoken: token
      }
    },
    columns: keysColDef
  });
}

createKeysTable();

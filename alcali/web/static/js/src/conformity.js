// Conformity Datatable.
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

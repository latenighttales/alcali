function manageKey(action, target) {
  showNotification('bg-black', '<b>action: </b>' + action + ' on ' + target + ' submitted', 'bottom', 'center');
  $.ajax({
    url: '/wheel',
    type: 'POST',
    data: {
      action: action,
      target: target,
      csrfmiddlewaretoken: token
    },

    // handle a successful response
    success: function(ret) {
      if (ret.hasOwnProperty('error')) {
        showNotification('bg-red', '<b>error: </b>' + ret.error, 'bottom', 'center');
      } else {
        showNotification('bg-black', '<b>action: </b>' + action + ' on ' + target + ' done', 'bottom', 'center');
        tableKeys.ajax.reload();
      }
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
  tableKeys = $('.js-basic-example').DataTable({
    responsive: true,
    "ajax": {
      "url": "/keys",
      "type": "POST",
      "data": {
        csrfmiddlewaretoken: token
      },
    },
    "columns": keysColDef
  });
}

createKeysTable();

function manageKey(action, target) {
  console.log(action, target);
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
      console.log(ret);
      if (ret.hasOwnProperty('error')) {
        showNotification('bg-red', 'error:' + ret.error, 'bottom', 'center');
      } else {
        window.location.reload();
      }
    },

    // handle a non-successful response
    error: function(xhr, errmsg, err) {
      console.log(errmsg);
      console.log(xhr.status + ': ' + xhr.responseText); // provide a bit more info about the error to the console
    }
  });
}

function createKeysTable() {
  $('.js-basic-example').DataTable({
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

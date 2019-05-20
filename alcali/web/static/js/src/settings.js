let userBtn = document.getElementById('userBtn');
userBtn.addEventListener('click', ev => {
  let formData = $('#user_form').serializeArray().reduce(function(obj, item) {
    obj[item.name] = item.value;
    return obj;
  }, {});
  formData.action = 'notifications';

  ev.preventDefault();
  $.ajax({
    type: 'POST',
    data: formData,

    // handle a successful response
    success: function(ret) {
      if (ret.result === 'updated') {
        showNotification(
          'bg-black',
          'User settings updated',
          'bottom',
          'center'
        );
      }
    },

    // handle a non-successful response
    error: function(xhr, errmsg, err) {
      // TODO: change for graph
      $('#results').html('<div class=\'alert-box alert radius\' data-alert>Oops! We have encountered an error: ' + errmsg +
        ' <a href=\'#\' class=\'close\'>&times;</a></div>'); // add the error to the dom
      console.log(xhr.status + ': ' + xhr.responseText); // provide a bit more info about the error to the console
    }
  });
});

let initDb = document.getElementById('init_db');
let minionListInit = document.getElementsByName('minions')[0];
let initDbTarget = '';
minionListInit.addEventListener('change', function() {
  initDb.disabled = false;
  initDbTarget = this.value;
});
initDb.addEventListener('click', ev => {
  ev.preventDefault();
  $.ajax({
    type: 'POST',
    data: {
      'action': 'init_db',
      'target': initDbTarget,
      csrfmiddlewaretoken: token
    },

    // handle a successful response
    success: function(ret) {
      if (ret.result === 'updated') {
        showNotification(
          'bg-black',
          'Function DB updated',
          'bottom',
          'center'
        );
      }
    },

    // handle a non-successful response
    error: function(xhr, errmsg, err) {
      // TODO: change for graph
      $('#results').html('<div class=\'alert-box alert radius\' data-alert>Oops! We have encountered an error: ' + errmsg +
        ' <a href=\'#\' class=\'close\'>&times;</a></div>'); // add the error to the dom
      console.log(xhr.status + ': ' + xhr.responseText); // provide a bit more info about the error to the console
    }
  });
});

let fieldDelete = document.getElementsByName('fieldDelete');
fieldDelete.forEach((btn) => {
  btn.addEventListener('click', function() {
    console.log(btn.value);
    $.ajax({
      type: 'POST',
      data: {
        'action': 'delete_field',
        'target': btn.value,
        csrfmiddlewaretoken: token
      },
      // handle a successful response
      success: function(ret) {
        if (ret.result) {
          showNotification(
            'bg-black',
            'Deleted minion field',
            'bottom',
            'center'
          );
        }
      },
      // handle a non-successful response
      error: function(xhr, errmsg, err) {
        // TODO: change for graph
        $('#results').html('<div class=\'alert-box alert radius\' data-alert>Oops! We have encountered an error: ' + errmsg +
          ' <a href=\'#\' class=\'close\'>&times;</a></div>'); // add the error to the dom
        console.log(xhr.status + ': ' + xhr.responseText); // provide a bit more info about the error to the console
      }

    });
  });
});

let fieldCreate = document.getElementById('fieldCreate');
fieldCreate.addEventListener('click', function(ev) {
  ev.preventDefault();
  let formData = $('#field_form').serializeArray().reduce(function(obj, item) {
    obj[item.name] = item.value;
    return obj;
  }, {});
  $.ajax({
    type: 'POST',
    data: formData,

    // handle a successful response
    success: function(ret) {
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
    error: function(xhr, errmsg, err) {
      // TODO: change for graph
      $('#results').html('<div class=\'alert-box alert radius\' data-alert>Oops! We have encountered an error: ' + errmsg +
        ' <a href=\'#\' class=\'close\'>&times;</a></div>'); // add the error to the dom
      console.log(xhr.status + ': ' + xhr.responseText); // provide a bit more info about the error to the console
    }
  });
});

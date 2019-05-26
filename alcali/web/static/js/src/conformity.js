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

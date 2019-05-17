/*
 POST on submit
 TODO: remove event listeners.
  */
var run = document.getElementById('run');
run.addEventListener('click', e => {
  salt_run('run');
  e.preventDefault();
});

var testRun = document.getElementById('test');
testRun.addEventListener('click', e => {
  e.preventDefault();
  salt_run('test');
});

function salt_run(type) {
  // Hide previous results.
  document.getElementById('results').style.display = 'none';

  // Dryrun.
  if (type === 'test') {
    var formData = $('form').serializeArray();
    formData.push({ name: 'test', value: 'true' });
  } else {
    formData = $('form').serialize();
  }

  // Notification.
  var funcName = document.getElementById('function_list').value;
  showNotification('bg-black', funcName + ' ' + 'submitted', 'bottom', 'center');

  // Ajax call.
  $.ajax({
    type: 'POST',
    data: formData,

    // handle a successful response
    success: function(yaml) {
      // remove the value from the input
      $('form').val('');
      let resDiv = document.getElementById('ansiResults');
      resDiv.innerHTML = yaml;
      toggleVisibility('results');
    },

    // handle a non-successful response
    error: function(xhr, errmsg, err) {
      $('#results').html(
        "<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " +
          errmsg +
          " <a href='#' class='close'>&times;</a></div>"
      ); // add the error to the dom
      console.log(xhr.status + ': ' + xhr.responseText); // provide a bit more info about the error to the console
    }
  });
}

// Functions tooltip
var functList = document.getElementById('function_list');

functList.addEventListener('change', () => {
  var selectedFunct = document.getElementById('function_list').value;
  $.ajax({
    type: 'POST',
    data: {
      tooltip: selectedFunct,
      csrfmiddlewaretoken: token
    },

    // handle a successful response
    success: function(docs) {
      // Set the selected function tooltip.
      var functToolTip = document.getElementById('funct_tooltip');
      functToolTip.title = selectedFunct;
      functToolTip.setAttribute('data-original-title', selectedFunct);
      functToolTip.setAttribute('data-content', '<pre>' + docs.desc + '</pre>');
      functToolTip.style.display = 'block';
    },

    // handle a non-successful response
    error: function(xhr, errmsg, err) {
      console.log(xhr.status + ': ' + xhr.responseText); // provide a bit more info about the error to the console
    }
  });
});

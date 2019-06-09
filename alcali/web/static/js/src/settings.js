/* Parse module button.
    Enabled on valid change.
 */
let initDb = document.getElementById('init_db');
let minionListInit = document.getElementsByName('minions')[0];
let initDbTarget = '';
function enableInitDb() {
  if (minionsList.includes(this.value)) {
    initDb.disabled = false;
    initDbTarget = this.value;
  } else {
    initDb.disabled = true;
    initDbTarget = '';
  }
}
minionListInit.addEventListener('change', enableInitDb);
minionListInit.addEventListener('input', enableInitDb);
initDb.addEventListener('click', ev => {
  if (initDbTarget !== '') {
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
  }
});

/*
  Add event listener on all buttons, and send a POST with this value.
  On success, delete the element from the dom.
  To be able to dynamically add event listener on newly created items, we add an attribute 'listener'.
 */
function deleteFields(type) {
  let fieldDelete = document.getElementsByName(type);
  fieldDelete.forEach((btn) => {
    // Add event listener only if not present
    if (btn.getAttribute('listener') !== 'true') {
      btn.setAttribute('listener', 'true');
      // On submit
      btn.addEventListener('click', function() {
        $.ajax({
          type: 'POST',
          data: {
            'action': type,
            'target': btn.value,
            csrfmiddlewaretoken: token
          },
          // handle a successful response
          success: function(ret) {
            if (ret.result) {
              document.getElementById(btn.value.replace(/\s/g, '')).outerHTML = "";
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
    }
  });
}
// On document ready, add event listeners.
deleteFields('delete_field');
deleteFields('delete_conformity');

function createFields(type) {
  let fieldCreate = document.getElementById('create_' + type);
  fieldCreate.addEventListener('click', function(ev) {
    ev.preventDefault();
    let formData = $('#form_' + type).serializeArray().reduce(function (obj, item) {
      obj[item.name] = item.value;
      return obj;
    }, {});
    formData.action = "create_" + type;
    $.ajax({
      type: 'POST',
      data: formData,

      // handle a successful response
      success: function(ret) {
        if (ret.result === 'updated') {
          // Get the template.
          let fieldTemplate = document.getElementById(type + 'Template');
          // Clone it.
          let clonedField = fieldTemplate.cloneNode(true);
          // Change clone inner elements.
          clonedField.getElementsByTagName('label')[0].innerText = formData['name'];
          clonedField.getElementsByTagName('code')[0].innerText = formData['function'];
          clonedField.getElementsByTagName('button')[0].value = formData['name'];
          clonedField.getElementsByTagName('button')[0].name = "delete_" + type;
          clonedField.id = formData['name'].replace(/\s/g, '');
          // Append in dom.
          fieldTemplate.parentNode.appendChild(clonedField);
          clonedField.style.display = 'block';
          // add event listener.
          deleteFields('delete_' + type);
          showNotification(
            'bg-black',
            type + ' created',
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
}
createFields('field');
createFields('conformity');

// User settings.
let userBtn = document.getElementById('userBtn');
userBtn.addEventListener('click', ev => {
  // Get form data.
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

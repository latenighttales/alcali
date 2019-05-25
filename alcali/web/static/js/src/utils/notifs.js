/*
  Notifs.
*/
let notifNb = document.getElementById('notif-nb');
let notifCount = notifNb.innerText || 0;

// Subscribe to events source.
let evtSource = new EventSource('/event_stream');

// Various Salt event tag matchers.
let isJobEvent = fnmatch('salt/job/*');
let isJobNew = fnmatch('salt/job/*/new');
let isJobReturn = fnmatch('salt/job/*/ret/*');

evtSource.onopen = function () {
  console.info('Listening ...')
};
evtSource.onerror = function (err) {
  console.error(err)
};
evtSource.onmessage = function (message) {

  let data = JSON.parse(message.data);

  if (isJobNew(data.tag) && notifPublished === 'True') {
    postNotification('published', data);
  } else if (isJobReturn(data.tag) && notifReturned === 'True') {
    postNotification('returned', data);
  } else if (isJobEvent(data.tag) && notifEvent === 'True') {
    postNotification('event', data);
  } else if (/^\w{20}$/.test(data.tag) && notifCreated === 'True') {
    postNotification('created', data);
  } else {
    /*    notifColor = 'bg-blue-grey';
        notifText = data.tag;*/
    return false;
  }
  // Notif Number
  notifCount += 1;
  notifNb.innerText = notifCount;
};

// Purge notifications on icon click.
let notifBtn = document.getElementById('notif-button');
notifBtn.addEventListener('click', (e) => {
  notifNb.innerText = '';
});

function postNotification(notifType, data) {
  // Get values from form.
  let postData = {'csrfmiddlewaretoken': token};
  postData['type'] = notifType;
  postData['tag'] = data.tag;
  postData['data'] = JSON.stringify(data.data);
  $.ajax({
    url: '/notifications',
    type: 'POST',
    data: postData,

    // handle a successful response
    success: function(ret) {
      let notifList = document.getElementById('notif-list');
      notifList.insertAdjacentHTML('afterbegin', ret);
    },

    // handle a non-successful response
    error: function(xhr, errmsg, err) {
      console.log(errmsg);
      console.log(xhr.status + ': ' + xhr.responseText); // provide a bit more info about the error to the console
    }
  });
}

function notifDelete(notifId) {

  $.ajax({
    url: '/notifications',
    type: 'POST',
    data: {
      'action': 'delete',
      'id': notifId,
      'csrfmiddlewaretoken': token,
    },

    // handle a successful response
    success: function (ret) {
      if (ret.result) {
        notifId = notifId === "*" ? "notif-list" : notifId;
        document.getElementById(notifId).outerHTML = "";
      }
    },

    // handle a non-successful response
    error: function (xhr, errmsg, err) {
      console.log(errmsg);
      console.log(xhr.status + ': ' + xhr.responseText); // provide a bit more info about the error to the console
    }
  });
}
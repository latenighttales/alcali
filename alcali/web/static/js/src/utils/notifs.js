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

  let notifList = document.getElementById('notif-list');

  let data = JSON.parse(message.data);

  // Defaults.
  let jid = data.data.jid;
  let notifColor = 'bg-default';
  let notifIcon = 'add';
  let notifText = 'unknown';
  let notifLink = '#';

  if (isJobNew(data.tag) && notifPublished === 'True') {
    notifColor = 'bg-blue';
    notifIcon = 'publish';
    notifText = '<b>' + data.data.fun + '</b> Published for ' + data.data.minions.length + ' Minion(s).';

  } else if (isJobReturn(data.tag) && notifReturned === 'True') {
    notifColor = 'bg-pink';
    notifIcon = 'subdirectory_arrow_left';
    notifText = '<b>' + data.data.fun + '</b> Returned for ' + data.data.id;
    notifLink = jid === undefined ? '' : '/jobs/' + jid + '/' + data.data.id;

    // On job return, if key event, refresh db.
    if (data.data.fun.match('wheel.key.(accept|reject|delete)')) {

    }

  } else if (isJobEvent(data.tag) && notifEvent === 'True') {
    notifColor = 'bg-amber';
    notifIcon = 'more_horiz';
    notifText = 'Job Event';

  } else if (/^\w{20}$/.test(data.tag) && notifCreated === 'True') {
    jid = data.tag;
    notifColor = 'bg-green';
    notifText = 'New Job Created';

  } else {
/*    notifColor = 'bg-blue-grey';
    notifText = data.tag;*/
    return false;

  }
  // Notif Number
  notifCount += 1;
  notifNb.innerText = notifCount;


  let date = new Date(data['data']['_stamp']).toLocaleString('en-EN').split(', ');
  let notifHtml = '<li>\n' +
    '                  <a href="' + notifLink + '" class=" waves-effect waves-block">\n' +
    '                    <div class="icon-circle ' + notifColor + '">\n' +
    '                      <i class="material-icons">' + notifIcon + '</i>\n' +
    '                    </div>\n' +
    '                    <div class="menu-info">\n' +
    '                      <h4>' + notifText + '</h4>\n' +
    '                      <p>\n' +
    '                        <i class="material-icons">access_time</i>' + date + '\n' +
    '                      </p>\n' +
    '                    </div>\n' +
    '                  </a>\n' +
    '                </li>';

  notifList.insertAdjacentHTML('afterbegin', notifHtml);
  // TODO:Keep only 6 last events DOES NOT WORK
  while (notifList.length > 6) {
    notifList.deleteRow(-1);
  }
};

// Purge notifications on icon click.
let notifBtn = document.getElementById('notif-button');
notifBtn.addEventListener('click', (e) => {
  notifNb.innerText = '';
});
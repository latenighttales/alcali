let currentJobNb = 0;
// Subscribe to events source.
let saltEvents = new EventSource("/event_stream");

// Alcali status.
saltEvents.onopen = function() {
  let wsAlert = document.getElementById("saltMasterWs");
  wsAlert.innerHTML = '<span class="label bg-green">OK</span>';
  console.info("connected to " + saltEvents.url);
};
saltEvents.onerror = function(err) {
  let wsAlert = document.getElementById("saltMasterWs");
  wsAlert.innerHTML = '<span class="label bg-red">NOT OK</span>';
  console.error(err);
};
saltEvents.onmessage = function(e) {
  let data = JSON.parse(e.data);
  // Current running jobs.
  if (isJobNew(data.tag)) {
    currentJobNb += data.data.minions.length;
  } else if (isJobReturn(data.tag)) {
    if (currentJobNb === 0) {
      currentJobNb = 0;
    } else currentJobNb -= 1;
    // Real time update chart.
    realtimeChart();
  }
  document.getElementById('running_jobs').innerText = currentJobNb;

  // Display only activated notifs.
  if ((isJobNew(data.tag) && notifPublished === 'True') ||
    (isJobReturn(data.tag) && notifReturned === 'True') ||
    (isJobEvent(data.tag) && notifEvent === 'True') ||
    (/^\w{20}$/.test(data.tag) && notifCreated === 'True')) {
    // Toggle event visibility.
    let rte = document.getElementById('rte');
    rte.style.display = 'block';

    // Main id: event tag.
    let tagId = data['tag'].split('/').join('');

    // Get panel Template and clone it.
    let panelTemplate = document.getElementById('panelTemplate');
    let clonedPanel = panelTemplate.cloneNode(true);
    clonedPanel.id = tagId + 'Panel';
    clonedPanel.style.display = 'block';

    // Heading.
    let headingTemplate = clonedPanel.querySelector('#headingTemplate');
    headingTemplate.id = tagId + 'Heading';

    let collapseTemplate = clonedPanel.querySelector('#collapseTemplate');
    collapseTemplate.id = tagId + 'Collapse';
    collapseTemplate.setAttribute('aria-labelledby', headingTemplate.id);

    let btnTemplate = clonedPanel.querySelector('#btnTemplate');
    btnTemplate.id = tagId + 'Btn';
    btnTemplate.setAttribute('href', '#' + collapseTemplate.id);
    btnTemplate.setAttribute('aria-controls', collapseTemplate.id);

    let titleTemplate = clonedPanel.querySelector('#titleTemplate');
    let eventDate = new Date(data['data']['_stamp'])
      .toLocaleString('en-EN')
      .split(', ');
    [data.tag, eventDate].forEach(data => {
      if (data) {
        let div = document.createElement('div');
        div.classList.add('col-lg-6', 'align-right');
        div.style.margin = '0';
        div.innerText = data;
        titleTemplate.appendChild(div);
      }
    });

    let formattedRet = clonedPanel.querySelector('#eventRet');
    formattedRet.value = JSON.stringify(data, undefined, 4);
    formattedRet.id = tagId;

    document.getElementById('rteBody').appendChild(clonedPanel);
    btnTemplate.click();
    mirrorify(tagId, 'application/json');

  } else {
    return false;
  }
};

// Jobs table.
$(function() {
  $(".js-exportable").DataTable({
    "order": [[0, "desc"]],
    searching: false,
    paging: false,
    info: false,
    buttons: false,
    dom: "<'row'<'col-sm-12'tr>>",
    responsive: false,
    "ajax": {
      "url": "/jobs",
      "type": "POST",
      "data": {csrfmiddlewaretoken: token, date: "", limit: "10"},
    },
    "columns": jobColDef
  });
});

function createProgress(id, data) {
  let progressBar = document.getElementById(id);
  let totalValue = Object.values(data).reduce((a, b)=> a + b, 0);
  let colorArr = Object.keys($.AdminBSB.options.colors);
  Object.values(data).forEach((value, index) => {
    let percent = Math.round(value / totalValue * 100);
    let conformityKeys = Object.keys(data);
    let conformityColor = colorArr[index * 2 + 5];
    if (['conflict', 'False'].indexOf(conformityKeys[index]) >= 0) {
      conformityColor = colorArr[0]
    }
    if (['None', 'unknown'].indexOf(conformityKeys[index]) >= 0) {
      return;
    }
    progressBar.innerHTML += '<div class="progress-bar bg-'+conformityColor+'" style="width: '+percent+'%" data-toggle="tooltip" title="'+conformityKeys[index]+': '+percent+'% ('+value+')" data-placement="bottom">\n' +
      '                          <span class="sr-only">'+percent+'</span>\n' +
      '                       </div>';
  });
}

let donutCharts = document.getElementById("donutCharts");
conformity.forEach((donut, index) => {
  donutCharts.innerHTML += '<div class="col-md-2">'+conformityName[index]+'</div>' +
    '<div class="col-md-10" style="margin-bottom: 0"><div class="progress" id="progress'+index+'"></div></div>';
  createProgress('progress' + index, donut)
});

$(function() {
  $(".card").matchHeight({
    byRow: true,
    property: "min-height",
    remove: false
  });
});

$('.progress-bar[data-toggle="tooltip"]').tooltip({
    animated: 'fade',
    placement: 'bottom'
});
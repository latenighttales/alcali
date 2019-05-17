// FAB.
let fab1 = document.getElementById('fab1');
let fabIcon = document.getElementById('fabIcon');
let innerFabs = document.getElementsByClassName('inner-fabs')[0];

fab1.addEventListener('click', function () {
  fabIcon.innerText = fabIcon.innerText !== 'add' ? 'add' : 'menu';
  innerFabs.classList.toggle('show')
});

document.addEventListener('click', function (e) {
  let fabTabs = ['fab1', 'fab2', 'fab3', 'fab4', 'fabIcon'];
  if (fabTabs.includes(e.target.id)) {
    return false;
  } else {
    fabIcon.innerText = 'menu';
    innerFabs.classList.remove('show');
  }
});

/*
  Check if browser supports local storage.
 */
function supports_local_storage() {
  try {
    return 'localStorage' in window && window['localStorage'] !== null;
  } catch (e) {
    return false;
  }
}

let sidebarToggled = JSON.parse(localStorage.getItem('sidebarToggled'));

if (supports_local_storage() === true) {
  if (sidebarToggled === true) {
    let leftSideBar = document.getElementById('leftsidebar');
    let contentSection = document.getElementsByClassName('content')[0];
    $('.sidebar .menu .list a span').each((idx, val) => {
      $(val).siblings().attr('data-toggle', 'tooltip');
      $(val).siblings().attr('data-placement', 'right');
      $(val).siblings().attr('title', $(val).text());
      $(val).hide();
    });
    $('[data-toggle="tooltip"]').tooltip({
      container: 'body'
    });
    //$('.sidebar .menu .list a span').hide();
    $('.sidebar .menu .list .header').hide();
    $('.sidebar .user-info .info-container .name').hide();
    $('.sidebar .user-info .info-container .email').hide();
    $('.sidebar .user-info .info-container .user-helper-dropdown').css({position: 'inherit'});
    leftSideBar.style.width = 55 + "px";
    contentSection.style.marginLeft = (55 + 15) + "px";
  }
}

// Mini Sidebar
$('#miniSidebar1').click(() => {
  sidebarToggled = JSON.parse(localStorage.getItem('sidebarToggled'));
  if (sidebarToggled === null) {
    localStorage.setItem('sidebarToggled', 'true');
    toggleSidebar(true);
  } else {
    localStorage.setItem('sidebarToggled', !sidebarToggled);
    toggleSidebar(sidebarToggled);
  }
});

/*$('#miniSidebar1').click(function () {
  sidebarToggled = JSON.parse(localStorage.getItem('sidebarToggled'));
  if (sidebarToggled === null) {
    $('.sidebar-toggle').toggle(300);
  } else {
    $('#leftsidebar').animate({
      width: 'toggle'
    }, 350);
  }
});*/


function toggleSidebar(toggled) {
  let leftSideBar = document.getElementById('leftsidebar');
  let contentSection = document.getElementsByClassName('content')[0];
  if (toggled === false) {
    let pos = 300;
    let id = setInterval(frameDown, 0);

    function frameDown() {
      if (pos === 55) {
        // Add tooltip to mini sidebar.
        $('.sidebar .menu .list a span').each((idx, val) => {
          $(val).siblings().attr('data-toggle', 'tooltip');
          $(val).siblings().attr('data-placement', 'right');
          $(val).siblings().attr('title', $(val).text());
          $(val).hide();
        });
        $('[data-toggle="tooltip"]').tooltip({
          container: 'body'
        });
        //$('.sidebar .menu .list a span').hide();
        $('.sidebar .menu .list .header').hide();
        $('.sidebar .user-info .info-container .name').hide();
        $('.sidebar .user-info .info-container .email').hide();
        $('#miniSidebar1 > div > div > div > span > b').hide();
        $('#miniSidebar1 > div > div > div > i').toggleClass('down');
        $('.sidebar .user-info .info-container .user-helper-dropdown').css({position: 'inherit'});
        clearInterval(id);
      } else {
        pos--;
        leftSideBar.style.width = pos + "px";
        contentSection.style.marginLeft = (pos + 15) + "px";
      }
    }
  } else {
    let pos = 55;
    let id = setInterval(frameUp, 0);

    function frameUp() {
      if (pos === 300) {
        $('.sidebar .menu .list a span').each((idx, val) => {
          $(val).siblings().removeAttr('data-toggle');
          $(val).siblings().removeAttr('data-placement');
          $(val).siblings().removeAttr('title');
          $(val).show();
        });
        $('.sidebar .menu .list .header').show();
        $('.sidebar .user-info .info-container .name').show();
        $('.sidebar .user-info .info-container .email').show();
        $('#miniSidebar1 > div > div > div > span > b').show();
        $('#miniSidebar1 > div > div > div > i').toggleClass('down');
        $('.sidebar .user-info .info-container .user-helper-dropdown').css({position: 'absolute'});
        clearInterval(id);
      } else {
        pos++;
        leftSideBar.style.width = pos + "px";
        contentSection.style.marginLeft = (pos + 15) + "px";
      }
    }
  }
}

$(function () {
  //Tooltip
  $('[data-toggle="tooltip"]').tooltip({
    container: 'body'
  });

  //Popover
  $('[data-toggle="popover"]').popover();
});

let jobColDef = [
  { name: "ID",
    render: function(data, type, row, meta) {
      if (type === "display") {
        data = '<a href="/jobs/' + data + '/'+ row[1] +'/">' + data + '</a>';
      }
      return data;
    }
  },
  { name: "Target",
    render: function(data, type, row, meta) {
      if (type === "display") {
        data = '<a href="/minions/' + data + '/">' + data + '</a>';
      }
      return data;
    }
  },
  { name: "Function" },
  { name: "Arguments" },
  { name: "User" },
  { name: "Status",
    render: function(data, type, row, meta) {
      if (type === "display") {
        if (data === true) {
          data = '<span class="label bg-green">Succeeded</span>';
        } else {
          data = '<span class="label label-danger">Failed</span>';
        }
      }
      return data;
    },
    className: "text-center"
  },
  { name: "Start Time",
    render: function(data, type, row, meta) {
      if (type === "display") {
        // TODO: use Locale locale..
        data = new Date(data).toLocaleString('en-GB');
      }
      return data;
    }
  },
  { name: "Actions",
    render: function(data, type, row, meta) {
      if (type === "display") {
        data = '<a href="/jobs/' + row[0] + '/'+ row[1] +'/" class="btn btn-primary btn-sm waves-effect" role="button">DETAIL</a>\n'+
          '<a href="/run?tgt=' + row[1] + '&fun='+ row[2] +'" class="btn bg-blue-grey btn-sm waves-effect" role="button">RERUN</a>';
      }
      return data;
    },
    className: "text-center"
  }
];

let minionColDef = [
  { name: "Minion Id",
    render: function(data, type, row, meta) {
      if (type === "display") {
        data = '<a href="/minions/' + data + '/">' + data + '</a>';
      }
      return data;
    }
  },
  { name: "Highstate Conformity",
    render: function(data, type, row, meta) {
      if (type === "display") {
        if (data === true) {
          data = '<span class="label bg-green">Conform</span>';
        } else {
          data = '<span class="label label-danger">Conflict</span>';
        }
      }
      return data;
    },
    className: "text-center"
  },
  { name: "Fqdn" },
  { name: "OS" },
  { name: "OS Version" },
  { name: "Kernel" },
  { name: "Last Job" },
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
  { name: "Action",
    render: function(data, type, row, meta) {
      if (type === "display") {
        data = '<button class="btn btn-primary btn-sm waves-effect" onclick="manageMinion(\'refresh\',\''+row[0]+'\')">REFRESH</button>\n';
        data += '<a href="/run?tgt='+row[0]+'" class="btn btn-sm bg-blue-grey waves-effect" role="button">RUN JOB</a>\n';
        data += '<button class="btn btn-danger btn-sm waves-effect" id="'+ row[0] +'" data-toggle="modal" data-target="#defaultModal">DELETE</button>\n';
      }
      return data;
    },
    className: "text-center"
  }
];

let keysColDef = [
  { name: "Minion id",
    render: function(data, type, row, meta) {
      if (type === "display") {
        if (row[1] === "accepted") {
          data = '<a href="/minions/' + data + '/">' + data + '</a>';
        }
      }
      return data;
    }
  },
  { name: "Key status",
    render: function(data, type, row, meta) {
      if (type === "display") {
        if (data === "accepted") {
          data = '<span class="label bg-green">'+data+'</span>';
        } else if (data === "rejected") {
          data = '<span class="label bg-red">'+data+'</span>';
        } else  if (data === "unaccepted") {
          data = '<span class="label bg-primary">'+data+'</span>';
        }
      }
      return data;
    },
    className: "text-center"
  },
  { name: "Public key" },
  { name: "Action",
    render: function(data, type, row, meta) {
      if (type === "display") {
        console.log(row[1]);
        if (row[1] === "accepted") {
          data = '<button class="btn btn-warning btn-sm waves-effect" onclick="manageKey(\'delete\', \''+row[0]+'\')">DELETE</button>\n';
          data += '<button class="btn btn-danger btn-sm waves-effect" onclick="manageKey(\'reject\', \''+row[0]+'\')">REJECT</button>\n';
        } else if (row[1] === "rejected") {
          data = '<button class="btn btn-success btn-sm waves-effect" onclick="manageKey(\'accept\', \''+row[0]+'\')">ACCEPT</button>\n';
          data += '<button class="btn btn-danger btn-sm waves-effect" onclick="manageKey(\'reject\', \''+row[0]+'\')">REJECT</button>\n';
        } else  if (row[1] === "unaccepted") {
          data = '<button class="btn btn-success btn-sm waves-effect" onclick="manageKey(\'accept\', \''+row[0]+'\')">ACCEPT</button>\n';
        }
      }
      return data;
    },
    className: "text-center"
  }
];
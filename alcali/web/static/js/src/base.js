/*
  FAB.
  There can be 4 fab mini buttons by pages.
 */
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
    $('#miniSidebar1 > div > div > div > span > b').hide();
    $('#miniSidebar1 > div > div > div > i').toggleClass('down');
    $('.sidebar .user-info .info-container .user-helper-dropdown').css({position: 'inherit'});
    leftSideBar.style.width = 55 + "px";
    contentSection.style.marginLeft = (55 + 15) + "px";
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

}


function toggleSidebar(toggled) {
  if (toggled === false) {
    // Add tooltip to mini sidebar.
    $('#leftsidebar').animate({width: '55px'}, 'fast', 'linear');
    $('#sectionContent').animate({marginLeft: '70px'}, 'fast', 'linear');
    $('.sidebar .menu .list a span').each((idx, val) => {
      $(val).siblings().attr('data-toggle', 'tooltip');
      $(val).siblings().attr('data-placement', 'right');
      $(val).siblings().attr('title', $(val).text());
      $(val).hide();
    });
    $('[data-toggle="tooltip"]').tooltip({
      container: 'body'
    });
    $('.sidebar .menu .list .header').hide();
    $('.sidebar .user-info .info-container .name').hide();
    $('.sidebar .user-info .info-container .email').hide();
    $('#miniSidebar1 > div > div > div > span > b').hide();
    $('#miniSidebar1 > div > div > div > i').toggleClass('down');
    $('.sidebar .user-info .info-container .user-helper-dropdown').css({position: 'inherit'});
  } else {
    $('#leftsidebar').animate({width: '300px'}, 'fast', 'linear');
    $('#sectionContent').animate({marginLeft: '315px'}, 'fast', 'linear');
    $('.sidebar .menu .list a span').each((idx, val) => {
      $(val).siblings().removeAttr('data-toggle');
      $(val).siblings().removeAttr('data-placement');
      $(val).siblings().removeAttr('data-original-title');
      $(val).siblings().removeAttr('title');
      $(val).show();
    });
    $('.sidebar .menu .list .header').show();
    $('.sidebar .user-info .info-container .name').show();
    $('.sidebar .user-info .info-container .email').show();
    $('#miniSidebar1 > div > div > div > span > b').show();
    $('#miniSidebar1 > div > div > div > i').toggleClass('down');
    $('.sidebar .user-info .info-container .user-helper-dropdown').css({position: 'absolute'});
  }
}

/*
  CLI MOTD.
 */
let cliMotdValue = JSON.parse(localStorage.getItem('cliMotd'));
if (cliMotdValue === true) {
  $("#cliMotd").prop('checked', true);
}

if (supports_local_storage() === true) {
  $("#cliMotd").change(function() {
    cliMotdValue = JSON.parse(localStorage.getItem("cliMotd"));
    if (cliMotdValue === null) {
      localStorage.setItem("cliMotd", "true");
    } else {
      localStorage.setItem("cliMotd", !cliMotdValue);
    }
  });
}

$(function () {
  //Tooltip
  $('[data-toggle="tooltip"]').tooltip({
    container: 'body'
  });

  //Popover
  $('[data-toggle="popover"]').popover();
});

// Job column definition.
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
          data = '<span class="label bg-green">SUCCEEDED</span>';
        } else {
          data = '<span class="label label-danger">FAILED</span>';
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

/*
  Keyboard shortcuts.
  Listen for "/", trigger showSearchBar if not already on input field.
 */
document.onkeyup = function(e) {
  e = e || window.event;
  let element;
  if (e.target) element = e.target;
  else if (e.srcElement) element = e.srcElement;
  if (element.nodeType == 3) element = element.parentNode;

  if (element.tagName == "INPUT" || element.tagName == "TEXTAREA") return;
  if (e.which === 191) {
    $.AdminBSB.search.showSearchBar();
  }
};

let minionTable;
function createMinionTable() {
  minionTable = $('.js-exportable').DataTable({
    "order": [[0, "desc"]],
    dom: "<'row'<'col-sm-2'l><'col-sm-5 pull-left'B><'col-sm-5'f>>" +
      "<'row'<'col-sm-12'tr>>" +
      "<'row'<'col-sm-6'i><'col-sm-6'p>>",
    responsive: true,
    buttons: [
      'colvis'
    ],
    "ajax": {
      "url": "/minions",
      "type": "POST",
      "data": {
        csrfmiddlewaretoken: token
      },
    },
    "columns": minionColDef
  });
}
createMinionTable();

// Delete minion modal.
$('#defaultModal').on('show.bs.modal', function(e) {
  let minion = e.relatedTarget.id;
  console.log(minion);
  let deleteBtn = document.getElementById('deleteMinion');
  deleteBtn.addEventListener('click', () => {
    manageMinion('delete', minion)
  });
});

/*
  Manage minions db.
  action: 'delete' TODO: restrain actions.
  minion: target. 'all' will target all minions.
 */
function manageMinion(action, minion) {
    showNotification('bg-black', '<b>action: </b>' + action + ' on ' + minion + ' submitted', 'bottom', 'center');
  // Ajax call.
  $.ajax({
    type: "POST",
    url: '/minions',
    data: {
      csrfmiddlewaretoken: token,
      minion: minion,
      action: action
    },

    // handle a successful response
    success: function (ret) {
      minionTable.ajax.reload();
      showNotification('bg-black', '<b>action: </b>' + action + ' on ' + minion + ' done', 'bottom', 'center');
    },

    // handle a non-successful response
    error: function (xhr, errmsg, err) {
      $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
        " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
      console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
  });
}


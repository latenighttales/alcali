function createMinionTable() {
  let table = $('.js-exportable').DataTable({
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

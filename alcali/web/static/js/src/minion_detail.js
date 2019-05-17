//displayJson(grainData, 'grain');

mirrorify('grain-yaml');
mirrorify('pillar-yaml');
customFields.forEach(field => {
  mirrorify(field + '-yaml');
});

//Exportable table
$('.js-exportable').DataTable({
  order: [[0, 'desc']],
  dom:
    "<'row'<'col-sm-6'l><'col-sm-6'f>>" +
    "<'row'<'col-sm-12'tr>>" +
    "<'row'<'col-sm-3'i><'col-sm-3 pull-left'B><'col-sm-6'p>>",
  responsive: true,
  buttons: ['copy', 'csv', 'excel', 'print'],
  "ajax": {
      "url": "/jobs",
      "type": "POST",
      "data": {
        limit: '100',
        csrfmiddlewaretoken: token,
        minion: minionId
      },
    },
    "columns": jobColDef
});

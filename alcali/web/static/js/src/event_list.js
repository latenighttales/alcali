$(function() {
  //Exportable table
  var table = $('.js-exportable').DataTable({
    responsive: true,
    columnDefs: [
      {
        targets: 6,
        render: function(data, type, row, meta) {
          return '' + JSON.stringify(JSON.parse(data), null, 4);
        }
      }
    ]
  });
});

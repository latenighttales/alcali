let jobTable = {};

function createJobTable() {
  // If we want to update table.
  if (jobTable.hasOwnProperty('destroy')) {
    jobTable.destroy();
  }
  // Get values from form.
  let postData = {};
  let formData = $("form").serializeArray();
  formData.forEach((data) => {
    // Remove empty fields.
    if (data['value'] !== '') {
      postData[data['name']] = data['value'];
    }
  });

  // create table.
  jobTable = $(".js-exportable").DataTable({
    "order": [[0, "desc"]],
    dom: "<'row'<'col-sm-6'l><'col-sm-6'f>>" +
      "<'row'<'col-sm-12'tr>>" +
      "<'row'<'col-sm-2'i><'col-sm-3 pull-left'B><'col-sm-7'p>>",
    responsive: true,
    buttons: [
      "copy", "csv", "excel", "print"
    ],
    "ajax": {
      "url": "/jobs",
      "type": "POST",
      "data": postData,
    },
    "columns": jobColDef
  });
}

// init flatpickr.
$(".flatpickr").flatpickr({
  mode: "range",
  maxDate: "today"

});

let btnSubmit = document.getElementById('btnSubmit');
btnSubmit.addEventListener("click", () => {
  createJobTable();
});

createJobTable();
// Backup create form.
let crudUser = document.getElementById("crud-user");
let createUserForm = crudUser.innerHTML;
// create table.
let userTable;
function createUserTable() {
  $.ajax({
    type: "POST",
    data: {
      csrfmiddlewaretoken: token,
      action: "list"
    },
    success: function(result) {
      //userTable.destroy();
      userTable = $(".js-exportable").DataTable({
        "order": [[0, "desc"]],
        dom: "<'row'<'col-sm-6'l><'col-sm-6'f>>" +
          "<'row'<'col-sm-12'tr>>" +
          "<'row'<'col-sm-2'i><'col-sm-3 pull-left'B><'col-sm-7'p>>",
        responsive: true,
        buttons: [
          "copy", "csv", "excel", "print"
        ],
        data: result.data,
        "columns": [
          { name: "Username" },
          { name: "First Name" },
          { name: "Last Name" },
          { name: "Email" },
          {
            name: "Token",
            render: function(data, type, row, meta) {
              if (type === "display") {
                data = '<button type="button" class="btn btn-primary waves-effect" id="' + data + '" data-toggle="modal" data-target="#showToken">VIEW</button>\n';
                data += '<button type="button" class="btn bg-blue-grey waves-effect" onclick="manageToken(\''+row[0]+'\', \'renew\')">RENEW</button>\n';
                data += '<button type="button" class="btn btn-danger waves-effect" onclick="manageToken(\''+row[0]+'\', \'revoke\')">REVOKE</button>\n';
              }
              return data;
            },
            className: "text-center"
          },
          { name: "Salt Permissions" },
          {
            name: "Last Login",
            render: function(data, type, row, meta) {
              if (type === "display") {
                // TODO: use Local locale..
                data = new Date(data).toLocaleString("en-GB");
              }
              return data;
            }
          },
          {
            name: "Actions",
            render: function(data, type, row, meta) {
              if (type === "display") {
                data = '<button type="button" class="btn btn-primary waves-effect edit-user" value="' + row[0] + '" id="' + row[0] +'edit">EDIT</button>\n';
                if (row[0] === currentUser) {
                  data += '<button type="button" class="btn btn-danger waves-effect" disabled>DELETE</button>\n';
                } else {
                  data += '<button type="button" class="btn btn-danger waves-effect" name="' + row[0] + '" data-toggle="modal" data-target="#deleteUser">DELETE</button>\n';
                }
              }
              return data;
            },
            className: "text-center"
          }
        ]
      });
    },
    complete: function() {
      addEditBtn();

    }
  });
}

/*
  addEditBtn

  Once Table is loaded, add event listener on every EDIT buttons.
  When clicked, fetch update form and insert in DOM.
 */
function addEditBtn() {
  let editUserBtn = document.getElementsByClassName("edit-user");
  Array.from(editUserBtn).forEach(function(btn) {
    let userBtnValue = btn.value;
    let currentBtn = document.getElementById(btn.id);
    currentBtn.addEventListener("click", function(evt) {
      evt.preventDefault();
      $.ajax({
        type: "GET",
        url: "/users/" + userBtnValue,
        success: function(result) {
          let crudUser = document.getElementById("crud-user");
          // Insert form in DOM.
          crudUser.innerHTML = result;
          $.AdminBSB.input.activate();
          // change box title.
          let boxTitle = document.getElementById('boxTitle');
          boxTitle.innerText = "EDIT " + userBtnValue;
          // change box icon.
          let userEditIcon = document.getElementById('userEditIcon');
          userEditIcon.innerText = 'mode_edit';

          let formSubmit = document.getElementById('formSubmit');
          formSubmit.addEventListener('click', function(e) {
            e.preventDefault();
            let formData = $('#user-form').serializeArray();
            $.ajax({
              type: "POST",
              url: "/users/" + userBtnValue,
              data: formData,
              success: function(result) {
                if (result.result === "success") {
                  showNotification("bg-black", "<b>action: </b>Update " + userBtnValue + " done", "bottom", "center");
                  userTable.destroy();
                  createUserTable();
                  crudUser.innerHTML = createUserForm;
                  $.AdminBSB.input.activate();
                }
              }
            });
          });
          // Add discard button.
          let userFormFooter = document.getElementById('userFormFooter');
          userFormFooter.innerHTML += '<button type="button" class="btn btn-default btn-lg m-l-15 waves-effect" id="discardChanges">DISCARD</button>';
          let discardChanges = document.getElementById('discardChanges');
          discardChanges.addEventListener('click', function() {
            crudUser.innerHTML = createUserForm;
            $.AdminBSB.input.activate();
          });
        }
      });
    });
  });
}
createUserTable();

// Delete minion modal.
$("#showToken").on("show.bs.modal", function(e) {
  let user = e.relatedTarget.id;
  let modalBody = document.getElementsByClassName("modal-body")[0];
  modalBody.innerHTML = user;
});

function manageToken(username, action) {
  $.ajax({
    type: "POST",
    "data": {
      csrfmiddlewaretoken: token,
      action: action,
      user: username
    },
    success: function(result) {
      if (result.result === "success") {
        showNotification("bg-black", "<b>action: </b>"+ action +" token for " + username + " done", "bottom", "center");
        userTable.destroy();
        createUserTable();
      }
    }
  });
}

// Delete minion modal.
$("#deleteUser").on("show.bs.modal", function(e) {
  let user = e.relatedTarget.name;
  let modalLabel = document.getElementById("defaultModalLabel");
  modalLabel.innerHTML = "Delete " + user + " ?";
  let deleteBtn = document.getElementById("deleteUserBtn");
  deleteBtn.addEventListener("click", () => {
    $.ajax({
      type: "POST",
      "data": {
        csrfmiddlewaretoken: token,
        action: "delete",
        user: user
      },
      success: function(result) {
        if (result.result === "success") {
          showNotification("bg-black", "<b>action: </b>delete " + user + " done", "bottom", "center");
          userTable.destroy();
          createUserTable();
          $("#closedeleteUserModal").trigger("click");
        }
      }
    });
  });
});

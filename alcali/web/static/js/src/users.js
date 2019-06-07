// create table.
function createUserTable() {
  $.ajax({
    type: 'POST',
    "data": {
      csrfmiddlewaretoken: token,
      action: "list"
    },
    success: function(result) {
      $(".js-exportable").DataTable({
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
          { name: 'Username' },
          { name: 'First Name' },
          { name: 'Last Name' },
          { name: 'Email' },
          { name: 'Token',
            render: function(data, type, row, meta) {
              if (type === 'display') {
                data = '<button type="button" class="btn btn-primary waves-effect">VIEW</button>\n';
                data += '<button type="button" class="btn bg-blue-grey waves-effect">RENEW</button>\n';
                data += '<button type="button" class="btn btn-danger waves-effect">REVOKE</button>\n';
              }
              return data;
            },
            className: 'text-center'
          },
          { name: 'Salt Permissions' },
          { name: 'Last Login',
            render: function(data, type, row, meta) {
              if (type === 'display') {
                // TODO: use Local locale..
                data = new Date(data).toLocaleString('en-GB');
              }
              return data;
            }
          },
          { name: 'Actions',
            render: function(data, type, row, meta) {
              if (type === 'display') {
                let userToken = data;
                data ='<button type="button" class="btn btn-primary waves-effect edit-user" value="' + row[0] + '">EDIT</button>\n';
                data += '<button type="button" class="btn btn-danger waves-effect">DELETE</button>\n';
              }
              return data;
            },
            className: 'text-center'
          }
        ]
      });
      let editUserBtn = document.getElementsByClassName('edit-user');

      Array.from(editUserBtn).forEach(function(btn) {
        let currentUser = btn.value;
        btn.addEventListener("click", function(evt) {
          evt.preventDefault();
          $.ajax({
            type: 'POST',
            url: '/users/' + currentUser,
            "data": {
              csrfmiddlewaretoken: token,
              action: "edit",
              user: currentUser,
            },
            success: function(result) {
              let crudUser = document.getElementById('crud-user');
              crudUser.innerHTML = result;
              let passwordFields = document.getElementById('password-fields');
              //passwordFields.innerHTML = "";
              $.AdminBSB.input.activate();
              let userForm = document.getElementById('user-form');
              userForm.setAttribute('action', "/users/" + currentUser);
            }
          });
        });
      });

    }
  });
}

createUserTable();

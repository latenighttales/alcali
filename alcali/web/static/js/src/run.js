/*
 POST on submit
  */
["run", "test"].forEach((runType) => {
  // Get btn.
  let btn = document.getElementById(runType);
  btn.addEventListener("click", ev => {
    ev.preventDefault();
    salt_run(runType)
  })
});

function salt_run(type) {
  let formData;
  // Hide previous results.
  document.getElementById("results").style.display = "none";

  // Dry run.
  if (type === "test") {
    formData = $("form").serializeArray();
    formData.push({ name: "test", value: "true" });
  } else {
    formData = $("form").serialize();
  }

  // Notification.
  let funcName = document.getElementById("function_list").value;
  showNotification(
    "bg-black",
    funcName + " " + "submitted",
    "bottom",
    "center"
  );

  // Ajax call.
  $.ajax({
    url: window.location.href.split("?")[0],
    type: "POST",
    data: formData,

    // handle a successful response
    success: function(yaml) {
      // remove the value from the input
      document.getElementById('salt-run').reset();
      let resDiv = document.getElementById("ansiResults");
      resDiv.innerHTML = yaml;
      toggleVisibility("results");
    },

    // handle a non-successful response
    error: function(xhr, errmsg, err) {
      $("#results").html(
        "<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " +
        errmsg +
        " <a href='#' class='close'>&times;</a></div>"
      ); // add the error to the dom
      console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
  });
}

let minionListInit = document.getElementById("minion_list");
let inputBackup = minionListInit.cloneNode(true);

let inputType = document.getElementById("target-type");
inputType.addEventListener("change", () => {
  let minionList = document.getElementById("minion_list");

  if (inputType.value === "custom") {
    minionList.outerHTML =
      '<div class="col" id="minion_list">' +
      '<input title="custom" name="custom" type="text" class="form-control btn-spaced" placeholder="glob target"></div>';
  } else if (inputType.value === "group") {
    minionList.outerHTML =
      '<input spellcheck="false" class="form-control" id="minion_list" name="minion_list" type="text"\n' +
      '                             list="minions"\n' +
      '                             placeholder="Target"/>\n' +
      '                      <datalist id="minions">\n' +
      '                      </datalist>';
    let groupOption = document.getElementById("minions");
    for (let key in nodeGroups) {
      let option = document.createElement("option");
      option.value = key;
      option.text = key;
      groupOption.appendChild(option);
    }
  } else if (inputType.value === "single") {
    minionList.outerHTML = inputBackup.outerHTML;
  }
});

// Functions tooltip
let functList = document.getElementById("function_list");

functList.addEventListener("change", () => {
  let selectedFunct = document.getElementById("function_list").value;
  $.ajax({
    type: "POST",
    data: {
      tooltip: selectedFunct,
      csrfmiddlewaretoken: token
    },

    // handle a successful response
    success: function(docs) {
      // Set the selected function tooltip.
      let functToolTip = document.getElementById("funct_tooltip");
      functToolTip.title = selectedFunct;
      functToolTip.setAttribute("data-original-title", selectedFunct);
      console.log(docs.desc);
      functToolTip.setAttribute("data-content", "<pre>" + docs.desc + "</pre>");
      functToolTip.style.display = "block";
    },

    // handle a non-successful response
    error: function(xhr, errmsg, err) {
      console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
  });
});

let args = document.getElementById("args");
let keyword = document.getElementById("keyword");
let argument = document.getElementById("argument");

if (getParams != null) {
  // Create a new 'change' event
  let event = new Event("change");

  // Fill run form with get params.
  minionListInit.value = getParams.hasOwnProperty("tgt")
    ? getParams.tgt[0]
    : "";
  delete getParams.tgt;
  functList.value = getParams.hasOwnProperty("fun") ? getParams.fun[0] : "";
  functList.dispatchEvent(event); // Dispatch event to show tooltip.
  delete getParams.fun;
  args.value = getParams.hasOwnProperty("args") ? getParams.args[0] : "";
  delete getParams.args;
  if (
    Object.entries(getParams).length !== 0 &&
    getParams.constructor === Object
  ) {
    Object.keys(getParams).forEach(key => {
      keyword.value = key;
      argument.value = getParams[key];
    });
  }
}

function addArgs() {
  let mainRow = document.getElementById("mainRow");
  let rowArgs =
    '' +
    ' <div class="col-lg-2 col-lg-offset-6">\n' +
    '   <div class="form-group">\n' +
    '     <div class="form-line" style="display: flex; flex-direction: row">\n' +
    '       <input title="args" id="args" name="args" type="text" class="form-control" placeholder="Args"/>\n' +
    '       <button type="button" class="btn btn-xs bg-blue-grey" onclick="addArgs()">\n' +
    '         <i class="material-icons">add</i>\n' +
    '       </button>\n' +
    '     </div>\n' +
    '   </div>\n' +
    ' </div>\n' +
    ' <div class="col-lg-2 p-r-0">\n' +
    '   <div class="form-group">\n' +
    '     <div class="form-line">\n' +
    '       <input title="keyword" id="keyword" name="keyword" type="text" class="form-control p-r-0"\n' +
    '              placeholder="Keyword"/>\n' +
    '     </div>\n' +
    '   </div>\n' +
    ' </div>\n' +
    ' <div class="col-lg-2 p-l-0">\n' +
    '   <div class="form-group">\n' +
    '     <div class="form-line" style="display: flex; flex-direction: row">\n' +
    '       <input title="argument" id="argument" name="argument" type="text" class="form-control p-l-0"\n' +
    '              placeholder="Argument"/>\n' +
    '       <button type="button" class="btn btn-xs bg-blue-grey" onclick="addArgs()">\n' +
    '         <i class="material-icons">add</i>\n' +
    '       </button>\n' +
    '     </div>\n' +
    '   </div>\n' +
    ' </div>';
  mainRow.insertAdjacentHTML('afterend', rowArgs);
}

let term = $("#terminal").terminal(function(command) {
  if (command !== "") {
    // Hide previous results.
    document.getElementById("results").style.display = "none";
    showNotification(
      'bg-black',
      command + ' ' + 'submitted',
      'bottom',
      'center'
    );
    $.ajax({
      type: "POST",
      url: window.location.href.split("?")[0],
      data: {
        csrfmiddlewaretoken: token,
        command: command
      },
      // handle a successful response
      success: function(yaml) {
        // remove the value from the input
        let resDiv = document.getElementById("ansiResults");
        resDiv.innerHTML = yaml;
        toggleVisibility("results");
      },

      // handle a non-successful response
      error: function(xhr, errmsg, err) {
        $("#results").html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
          " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
    });
  } else {
    this.echo("");
  }
}, {
  greetings: null,
  name: "js_demo",
  height: 300,
  prompt: "$ > ",
  completion: function(string, callback) {
    if (
      this.get_command().match(/^salt /)
      && minions.includes(this.get_command().split(" ").slice(-2)[0])
      && string.length >= 2
    ) {
      callback(func);
    }
    else if (this.get_command().match(/^salt /)) {
      callback(minions);
    } else {
      callback(["salt"]);
    }
  }
});

$(".flatpickr").flatpickr({
  enableTime: true,
  minDate: "today"

});

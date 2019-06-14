/*
 POST on submit
  */
["run", "test"].forEach((runType) => {
  // Get btn.
  let btn = document.getElementById(runType);
  btn.addEventListener("click", ev => {
    ev.preventDefault();
    salt_run(runType);
  })
});

/*
  Populate options depending on the client type, and hide non relevant fields.
 */
let clientType = document.getElementById('client');
clientType.addEventListener('change', function (ev) {
  let clientFunc = document.getElementById('client_function');
  clientFunc.innerHTML = "";

  if (this.value === "local") {
    localFunc.forEach(val => {
      clientFunc.innerHTML += '<option value="' + val + '">' + val;
    });
    document.getElementById('salt-target').style.display = "block";
  } else if (this.value === "wheel") {
    wheelFunc.forEach(val => {
      clientFunc.innerHTML += '<option value="' + val + '">' + val;
    });
    document.getElementById('salt-target').style.display = "none";
  } else if (this.value === "runner") {
    runnerFunc.forEach(val => {
      clientFunc.innerHTML += '<option value="' + val + '">' + val;
    });
    document.getElementById('salt-target').style.display = "none";
  }
});

/*
  Run job.
 */
function salt_run(type) {
  let data = $("form").serializeArray().reduce(function(obj, item) {
    obj[item.name] = item.value;
    return obj;
  }, {});
  // Hide previous results.
  document.getElementById("results").style.display = "none";

  // Dry run.
  if (type === "test") {
    data.test = true
  }

  // schedule
  if (data['schedule-sw'] === 'on') {
    data['schedule_type'] = scheduleType;
    data.cron = cronField.cron("value")

  }

  // Notification.
  let funcName = document.getElementById("function_list").value;
  showNotification(
    "bg-black",
    funcName + " submitted",
    "bottom",
    "center"
  );

  // Ajax call.
  $.ajax({
    url: window.location.href.split("?")[0],
    type: "POST",
    data: data,


    // handle a successful response
    success: function(yaml) {
      // remove the value from the input
      // TODO: fix switch not being reset.
      //document.getElementById('salt-run').reset();
      // Insert result html.
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

// Change target input depending on target type.
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

/*
  Retrieve functions tooltip
 */
let functList = document.getElementById("function_list");
functList.addEventListener("change", () => {
  let selectedFunct = document.getElementById("function_list").value;
  $.ajax({
    type: "POST",
    data: {
      tooltip: selectedFunct,
      client: clientType.value,
      csrfmiddlewaretoken: token
    },

    // handle a successful response
    success: function(docs) {
      // Set the selected function tooltip.
      let functToolTip = document.getElementById("funct_tooltip");
      functToolTip.title = selectedFunct;
      functToolTip.setAttribute("data-original-title", selectedFunct);
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

/*
  Insert params in fields if there's get arguments.
 */
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
    // Insert kwargs.
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

/*
  CLI
 */
let greetings = [
  "60% of the time, it works every time!",
  "srsly dude, why?",
  " _________________\n" +
  "( I'm a moooodule )\n" +
  " -----------------\n" +
  "        o   ^__^\n" +
  "         o  (oO)\\_______\n" +
  "            (__)\\       )\\/\\\n" +
  "             U  ||----w |\n" +
  "                ||     ||",
  "Don't Panic.",
  "I'm sorry, Dave. I'm afraid I can't do that.",
  "If your return is not back in five minutes, just wait longer.",
  "Cool. Cool,Cool,Cool.",
  "I find your lack of faith disturbing.",
  "Worst. CLI. Ever.",
];

let term = $("#terminal").terminal(function(command) {
  if (command !== "") {
    // Wrong command handling.
    if (command.split(" ").length <= 2 || command.split(" ")[0] !== "salt") {
      this.echo("Missing arguments or improper usage");
      return false;
    }
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
  greetings: greetings[Math.floor(Math.random() * greetings.length)] + "\n",
  name: "js_demo",
  height: 300,
  prompt: "$ > ",
  completion: function(string, callback) {
    if (
      this.get_command().match(/^salt /)
      && minions.includes(this.get_command().split(" ").slice(-2)[0])
      && string.length >= 2
    ) {
      // TODO: ARGS, KWARGS?
      callback(localFunc);
    }
    else if (this.get_command().match(/^salt /)) {
      callback(minions);
    } else {
      callback(["salt"]);
    }
  }
});

// Init flatpickr.
$(".flatpickr").flatpickr({
  enableTime: true,
  minDate: "today"

});
let cronField = $('#cronSelector').cron({
  initial: '0 0 * * *',
  customValues: {
    'half hour': '*/30 * * * *'
  }
});

let scheduleType = 'recurrent';
$("input[name='group1']:radio").change(function() {
  if (document.getElementById("radio_1").checked) {
    scheduleType = 'recurrent';
    document.getElementById("cronSchedule").style.display = "block";
    document.getElementById("dateSchedule").style.display = "none";
  } else {
    scheduleType = 'once';
    document.getElementById("cronSchedule").style.display = "none";
    document.getElementById("dateSchedule").style.display = "block";
  }
});

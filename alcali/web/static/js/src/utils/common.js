/*
  Function to toggle visibility
  input: <ID>
 */
function toggleVisibility(id) {
  let e = document.getElementById(id);
  e.style.display = e.style.display !== 'none' ? 'none' : 'block';
}

/* function to allow Salt-style globbing on event tags. */
function fnmatch(pattern) {
  if (pattern.indexOf('*') === -1) {
    return filename => pattern === filename;
  } else {
    // Taken from Lodash (MIT).
    // Use _.escapeRegExp directly if available.
    let reRegExpChar = /[\\^$.*+?()[\]{}|]/g;
    let escaped = pattern.replace(reRegExpChar, '\\$&');
    let matcher = new RegExp('^' + escaped.replace(/\\\*/g, '.*') + '$');
    return filename => matcher.test(filename);
  }
}

function sortJson(unordered) {
  const ordered = {};
  Object.keys(unordered).sort().forEach(function (key) {
    ordered[key] = unordered[key];
  });
  return ordered;
}

/*
  CodeMirror helper.
 */
function mirrorify(id, mode = "yaml") {
  CodeMirror.fromTextArea(document.getElementById(id), {
    mode: mode,
    theme: "made-of-code",
    autoRefresh: true,
    lineNumbers: false,
    readOnly: true,
    cursorBlinkRate: 0,
    //viewportMargin: Infinity,
    foldGutter: true,
    gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter"],

  });
}

/*
  Manage minions db.
  action: 'delete' TODO: restrain actions.
  minion: target. 'all' will target all minions.
 */
function manageMinion(action, minion) {
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
      console.log(ret);
      location.reload();
    },

    // handle a non-successful response
    error: function (xhr, errmsg, err) {
      $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
        " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
      console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
  });
}

/*
  Refresh Keys.
 */
function refreshKeys() {
  // Ajax call.
  $.ajax({
    type: "POST",
    url: '/keys',
    data: {
      csrfmiddlewaretoken: token,
      action: 'refresh',
    },

    // handle a successful response
    success: function () {
      location.reload();
    },

    // handle a non-successful response
    error: function (xhr, errmsg, err) {
      $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
        " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
      console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
  });

}

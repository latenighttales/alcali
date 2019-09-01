/*
 * Version: 0.1
 * Usage:
 * Create the ui by initiating new instance of `CronUI`.
 * Pass in the selector for the container element of the form,
 * and an options object.
 *
 * recurrentEventForm = new CronUI('.container', {initial: '* * * * *'});
 */
function CronUI(container, opts) {
  if (container instanceof HTMLElement) {
    this.el = container
  } else if (typeof container === "string") {
    this.el = document.querySelector(container)
  } else {
    throw "CronUI: container parameter in initialization must be an html element or a string selector."
  }

  // init options
  this.options = opts ? opts : {} /* default to empty obj */

  // Render the cron form
  this.render()

  // Make sure there is an initial value and set it on.
  if (typeof this.options.initial !== "string") {
    this.options.initial = "* * * * *"
  }
  this.setCronString(this.options.initial)
  this.currentValue = this.options.initial
}


CronUI.prototype.render = function() {
  let suffix
  let j
  let i
  let el = this.el

  // -------  build some static data -------

  // options for minutes in an hour
  let str_opt_mih = ""
  for (i = 0; i < 60; i++) {
    j = (i < 10) ? "0" : ""
    str_opt_mih += "<option value='" + i + "'>" + j + i + "</option>\n"
  }

  // options for hours in a day
  let str_opt_hid = ""
  for (i = 0; i < 24; i++) {
    j = (i < 10) ? "0" : ""
    str_opt_hid += "<option value='" + i + "'>" + j + i + "</option>\n"
  }

  // options for days of month
  let str_opt_dom = ""
  for (i = 1; i < 32; i++) {
    if (i == 1 || i == 21 || i == 31) {
      suffix = "st"
    } else if (i == 2 || i == 22) {
      suffix = "nd"
    } else if (i == 3 || i == 23) {
      suffix = "rd"
    } else {
      suffix = "th"
    }
    str_opt_dom += "<option value='" + i + "'>" + i + suffix + "</option>\n"
  }

  // options for months
  let str_opt_month = ""
  const months = ["January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"]
  for (i = 0; i < months.length; i++) {
    str_opt_month += "<option value='" + (i + 1) + "'>" + months[i] + "</option>\n"
  }

  // options for day of week
  let str_opt_dow = ""
  const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday"]
  for (i = 0; i < days.length; i++) {
    str_opt_dow += "<option value='" + i + "'>" + days[i] + "</option>\n"
  }

  // options for period
  let str_opt_period = ""
  const periods = ["minute", "hour", "day", "week", "month", "year"]
  for (i = 0; i < periods.length; i++) {
    str_opt_period += "<option value='" + periods[i] + "'>" + periods[i] + "</option>\n"
  }


  // ---- define select boxes in the right order -----
  let blocks = {}

  // Period
  el.insertAdjacentHTML("beforeend",
    "<span class='cron-period'><select>" + str_opt_period + "</select></span>")
  let periodEl = el.querySelector(".cron-period select")
  periodEl.addEventListener("change", this.periodChanged.bind(this))
  periodEl.addEventListener("change", this.changeEvent.bind(this))

  // Day of month
  el.insertAdjacentHTML("beforeend", "<span class='cron-block cron-block-dom'>"
    + " on the <select name='cron-dom'>" + str_opt_dom
    + "</select> </span>")
  blocks["dom"] = el.querySelector(".cron-block-dom")

  // Month
  el.insertAdjacentHTML("beforeend", "<span class='cron-block cron-block-month'>"
    + " of <select name='cron-month'>" + str_opt_month
    + "</select> </span>")
  blocks["month"] = el.querySelector(".cron-block-month")

  // Minutes
  el.insertAdjacentHTML("beforeend", "<span class='cron-block cron-block-mins'>"
    + " at <select name='cron-mins'>" + str_opt_mih
    + "</select> minutes past the hour </span>")
  blocks["mins"] = el.querySelector(".cron-block-mins")

  // Day of week
  el.insertAdjacentHTML("beforeend", "<span class='cron-block cron-block-dow'>"
    + " on <select name='cron-dow'>" + str_opt_dow
    + "</select> </span>")
  blocks["dow"] = el.querySelector(".cron-block-dow")

  // Time
  el.insertAdjacentHTML("beforeend", "<span class='cron-block cron-block-time'>"
    + " at <select name='cron-time-hour' class='cron-time-hour'>" + str_opt_hid
    + "</select>:<select name='cron-time-min' class='cron-time-min'>" + str_opt_mih
    + " </span>")
  blocks["time"] = el.querySelector(".cron-block-time")

  // Atttach the change event to all selectors
  for (let blockName in blocks) {
    [].forEach.call(blocks[blockName].querySelectorAll("select"), function(selectEl) {
      selectEl.addEventListener("change", this.changeEvent.bind(this))
    }.bind(this))
  }

  // Save a reference to blocks
  this.blocks = blocks
}

CronUI.prototype.periodChanged = function() {
  let blocks = this.blocks
  let cronPeriodEl = this.el.querySelector(".cron-period select")
  let period = cronPeriodEl.options[cronPeriodEl.selectedIndex].value

  // Hide all current blocks
  for (let blockName in blocks) {
    blocks[blockName].style.display = "none"
  }

  // Show only blocks that needs to be shown by the period chosen
  if (CronUI.displayMatrix.hasOwnProperty(period)) {
    let b = CronUI.displayMatrix[period]
    for (let i = 0; i < b.length; i++) {
      blocks[b[i]].style.display = ""
    }
  }
}

// The `changeEvent` is fired whenever there is a form change.
// It updates the `currentValue` of cron string and optionally calls
// a user set callback.
CronUI.prototype.changeEvent = function() {
  this.currentValue = this.getCronString()
  if (typeof this.options.changeEvent === "function") {
    this.options.changeEvent(this.currentValue)
  }
}


CronUI.prototype.getCronString = function() {
  let min, hour, day, month, dow
  min = hour = day = month = dow = "*"
  let blocks = this.blocks
  // Helper to get value from select fields
  let getSelectValue = function(el) {
    return el.options[el.selectedIndex].value
  }

  let selectedPeriod = getSelectValue(this.el.querySelector(".cron-period select"))
  switch (selectedPeriod) {
    case "minute":
      break

    case "hour":
      min = getSelectValue(blocks["mins"].querySelector("select"))
      break

    case "day":
      min = getSelectValue(blocks["time"].querySelector(".cron-time-min"))
      hour = getSelectValue(blocks["time"].querySelector(".cron-time-hour"))
      break

    case "week":
      min = getSelectValue(blocks["time"].querySelector(".cron-time-min"))
      hour = getSelectValue(blocks["time"].querySelector(".cron-time-hour"))
      dow = getSelectValue(blocks["dow"].querySelector("select"))
      break

    case "month":
      min = getSelectValue(blocks["time"].querySelector(".cron-time-min"))
      hour = getSelectValue(blocks["time"].querySelector(".cron-time-hour"))
      day = getSelectValue(blocks["dom"].querySelector("select"))
      break

    case "year":
      min = getSelectValue(blocks["time"].querySelector(".cron-time-min"))
      hour = getSelectValue(blocks["time"].querySelector(".cron-time-hour"))
      day = getSelectValue(blocks["dom"].querySelector("select"))
      month = getSelectValue(blocks["month"].querySelector("select"))
      break

    default:
      // we assume this only happens when customValues is set
      return selectedPeriod
  }
  return [min, hour, day, month, dow].join(" ")
}

CronUI.prototype.setCronString = function(cronString) {
  let blocks = this.blocks
  let cronType = CronUI.getCronType(cronString)

  if (!cronType) {
    return false
  }

  let d = cronString.split(" ")
  let v = {
    "mins": d[0],
    "hour": d[1],
    "dom": d[2],
    "month": d[3],
    "dow": d[4],
  }

  // update appropriate select boxes
  let targets = CronUI.displayMatrix[cronType]
  for (let i = 0; i < targets.length; i++) {
    let tgt = targets[i]
    if (tgt == "time") {
      blocks[tgt].querySelector(".cron-time-hour").value = v["hour"]

      blocks[tgt].querySelector(".cron-time-min").value = v["mins"]
    } else {
      blocks[tgt].querySelector("select").value = v[tgt]
    }
  }

  // Update the period select box
  this.el.querySelector(".cron-period select").value = cronType
  this.periodChanged()

  return this
}

// Static functions and settings
// --------------------------------------------------

CronUI.displayMatrix = {
  "minute": [],
  "hour": ["mins"],
  "day": ["time"],
  "week": ["dow", "time"],
  "month": ["dom", "time"],
  "year": ["dom", "month", "time"],
}

CronUI.cronTypes = {
  "minute": /^(\*\s){4}\*$/,                    // "* * * * *"
  "hour": /^\d{1,2}\s(\*\s){3}\*$/,           // "? * * * *"
  "day": /^(\d{1,2}\s){2}(\*\s){2}\*$/,      // "? ? * * *"
  "week": /^(\d{1,2}\s){2}(\*\s){2}\d{1,2}$/, // "? ? * * ?"
  "month": /^(\d{1,2}\s){3}\*\s\*$/,           // "? ? ? * *"
  "year": /^(\d{1,2}\s){4}\*$/,                // "? ? ? ? *"
}

CronUI.getCronType = function(cronString) {
  // Try for provided cron string, and fallback to the instance cron string
  cronString = cronString ? cronString : this.getCronString()

  // check format of initial cron value
  const valid_cron = /^((\d{1,2}|\*)\s){4}(\d{1,2}|\*)$/
  if (typeof cronString != "string" || !valid_cron.test(cronString)) {
    return undefined
  }

  // check actual cron values
  let d = cronString.split(" ")
  //            mm, hh, DD, MM, DOW
  let minval = [0, 0, 1, 1, 0]
  let maxval = [59, 23, 31, 12, 6]
  for (var i = 0; i < d.length; i++) {
    if (d[i] == "*") continue
    var v = parseInt(d[i])
    if (v <= maxval[i] && v >= minval[i]) continue
    // If we got here, the value is violating some rule. exit.
    return undefined
  }

  // determine combination
  for (let type in CronUI.cronTypes) {
    if (CronUI.cronTypes[type].test(cronString)) {
      return type
    }
  }

  // unknown combination
  return undefined
}

export default CronUI

var shortTimeoutCallback = function() {
  console.log("shortTimeout: done");
  document.getElementById("shorttimeout-result").innerHTML = "executed at least once";
}

var shortTimeoutTrigger = function () {
  console.log("shortTimeout: triggered");
  document.getElementById("shorttimeout-result").innerHTML = "running";
  setTimeout(shortTimeoutCallback, 4000)
}

var fetchCallback = function () {
  console.log("fetch: done")
  document.getElementById("fetch-result").innerHTML = "executed at least once";
}

var fetchTrigger= function() {
  console.log("fetch: triggered");
  document.getElementById("fetch-result").innerHTML = "running";
  var result = fetch("/fetch",{
    cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
  }).then(fetchCallback)
}

var xhrCallback = function () {
  console.log("xhr: done");
  document.getElementById("xhr-result").innerHTML = "executed at least once";
}

var xhrTrigger= function() {
  console.log("xhr: triggered");
  document.getElementById("xhr-result").innerHTML = "running";
  var xhr = new XMLHttpRequest();
  xhr.open("GET","/fetch", true);
  xhr.onload = xhrCallback;
  xhr.send();
}

var testabilityReadyCallback = function () {
  console.log("testabilityReadyCallback: triggered");
}

var transitionTrigger = function () {
  console.log("transition: triggered");
  document.getElementById("transition-result").innerHTML = "running";
  $('.crossRotate').toggleClass('active');
  setTimeout(transitionCallback, 4000)
}

var transitionCallback= function () {
  console.log("transition: done");
  document.getElementById("transition-result").innerHTML = "executed at least once";
  $('.crossRotate').toggleClass('active');
  window.testability.wait.oneLess()
}

var animateTrigger = function () {
  console.log("animate: triggered");
  document.getElementById("animate-result").innerHTML = "running";
  $('.animateBox').toggleClass('active');
  setTimeout(animateCallback, 4000)
}

var animateCallback= function () {
  console.log("animate: done");
  document.getElementById("animate-result").innerHTML = "executed at least once";
  $('.animateBox').toggleClass('active');
  window.testability.wait.oneLess()
}


var allowDrop = function(ev) {
  ev.preventDefault();
}

var drag = function(ev) {
  ev.dataTransfer.setData("text", ev.target.id);
}

var drop = function(ev) {
  ev.preventDefault();
  var data = ev.dataTransfer.getData("text");
  ev.target.appendChild(document.getElementById(data));
}

var redirectTrigger = function() {
  console.log("redirect: trigger");
  var cur = encodeURIComponent(window.location + "/sub")
  var redirurl = "https://httpbin.org/redirect-to?url=" + cur + "&status_code=302"
  window.location = redirurl
}

var storageTrigger = function() {
  var testObj = {
    "number": 1,
    "str": "snafu",
    "boolean": true,
    "array": [1,2,3,4,5]
  }
  window.localStorage.setItem("simple_key_str", "simple_key_str_value")
  window.sessionStorage.setItem("simple_key_str", "simple_key_str_value")

  window.localStorage.setItem("simple_key_bool", true)
  window.sessionStorage.setItem("simple_key_bool", true)

  window.localStorage.setItem("simple_key_int", 31337)
  window.sessionStorage.setItem("simple_key_bool", 31337)

  window.localStorage.setItem("json_key", JSON.stringify(testObj))
  window.sessionStorage.setItem("json_key", JSON.stringify(testObj))
}
var logTrigger = function() {
  console.log("LOGTRIGGER: log")
  console.error("LOGTRIGGER: error")
  console.debug("LOGTRIGGER: debug")
  console.trace("LOGTRIGGER: trace")
  console.info("LOGTRIGGER: info")
  logTriggerError()
}


storageTrigger()

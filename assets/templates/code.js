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

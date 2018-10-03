var simpleButtonCallback = function() {
  console.log("simpleButtonCallback: triggered");
}

var fetchCallback = function() {
  console.log("fetchCallback: triggered");
  var result = fetch("/fetch",{
    cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
  }).then(function()  { console.log("fetchCallback: done") } );
}

var xhrCallback = function() {
  console.log("xhrCallback: triggered");
  var xhr = new XMLHttpRequest();
  xhr.open("GET","/fetch", true);
  xhr.onload = function() {
   console.log("xhrCallback: done");
  };
  xhr.send();
}

var testabilityReadyCallback = function () {
  console.log("testabilityReadyCallback: triggered");
}

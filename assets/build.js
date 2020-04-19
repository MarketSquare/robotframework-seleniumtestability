window.simulateDragDrop = require('./simulateDragAndDrop').simulateDragDrop;
window.scrollStop = require('./scrollStop').scrollStop
window.testability = require('testability.js')
window.instrumentBrowser = require('testability-browser-bindings')
window.instrumentBrowser(window, "testability_config" in window ? window.testability_config : {})
window.scrollStop()
window.seleniumtestabilityready = true

window.simulateDragDrop = require('./simulateDragAndDrop').simulateDragDrop;
window.scrollStop = require('./scrollStop').scrollStop
window.testability = require('testability.js')
window.instrumentBrowser = require('testability-browser-bindings')
window.instrumentBrowser(window)
window.scrollStop()
window.seleniumtestabilityready = true

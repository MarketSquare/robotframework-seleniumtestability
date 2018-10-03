*** Settings ***
Library         SeleniumLibrary

*** Variables ***
${URL}   http://localhost:5000

*** Keywords ***
Instrument Browser
  Execute Javascript          instrumentBrowser(window)

Wait For Testability Ready
  Log To Console              Wait For Testability Ready
  Execute Async Javascript    var cb = arguments[arguments.length - 1]; window.testability.when.ready(function() {cb()});

*** Test Cases ***
Run Poc

  Set Selenium Timeout        20 seconds
  Open Browser                ${URL}    browser=Firefox
  Instrument Browser

  Log To Console              Click fetch-button
  Click Element               id:fetch-button

  Wait For Testability Ready

  Log To Console              Click shorttimeout-button
  Click Element               id:shorttimeout-button

  Wait For Testability Ready

  Log To Console              Click xhr-button
  Click Element               id:xhr-button

  Wait For Testability Ready

  Log To Console              All Done
  Sleep                       5 seconds
  [Teardown]                  Close Browser




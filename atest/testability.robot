*** Settings ***
Library         SeleniumTestability
Library         DateTime
Library         Process
Test Setup      Setup Test Environment
Test Teardown   Teardown Test Environment


*** Variables ***
${URL}        http://localhost:5000
${BROWSER}    Firefox
${TIMEOUT}    4.0

${INJECT_FROM_RF}     0

${FLASK_HANDLE}   None

*** Keywords ***
Start Flask App
  ${FLASK_HANDLE}=            Start Process   flask   run   shell=True    cwd=${EXEC_DIR}/assets

Stop Flask App
  Terminate Process           ${FLASK_HANDLE}   kill=True

Setup Test Environment
  Start Flask App
  ${URL}=   Set Variable    ${URL}?inject=${INJECT_FROM_RF}
  Set Selenium Timeout        120 seconds
  Log To Console              About to open ${BROWSER} with url ${URL}
  Open Browser                ${URL}    browser=${BROWSER}
  Run Keyword If    ${INJECT_FROM_RF}==1   Inject Testability
  Instrument Browser

Teardown Test Environment
  Stop Flask App
  Close Browser

#Inject Testability
#  Execute Javascript          ${EXEC_DIR}/www/api.js
#  Execute Javascript          ${EXEC_DIR}/www/bindings.js

#Instrument Browser
#  Execute Javascript          instrumentBrowser(window)

#Wait For Testability Ready
#  Sleep                       0.05 seconds
#  Log To Console              Wait For Testability Ready: Waiting
#  Execute Async Javascript    var cb = arguments[arguments.length - 1]; window.testability.when.ready(function() {cb()});
#  Log To Console              Wait For Testability Ready: Done

Click And Verify
  [Arguments]   ${id}    ${duration}
  Log To Console              Click ${id}
  ${start}=   Get Time        epoch
  Click Element               id:${id}
  Wait For Testability Ready
  ${end}=   Get Time        epoch
  ${diff}=  Subtract Date From Date   ${end}  ${start}
  Should Be True              not ${diff} < ${duration}

*** Test Cases ***
Test Fetch
  [Tags]    manual
  Click And Verify            fetch-button          ${TIMEOUT}

Test Timeout
  [Tags]    manual
  Click And Verify            shorttimeout-button   ${TIMEOUT}

Test XHR
  [Tags]    manual
  Click and Verify            xhr-button            ${TIMEOUT}

Test transition
  [Tags]    manual
  Click and Verify            transition-button     ${TIMEOUT}

Test Animation
  [Tags]    manual
  Click and Verify            animate-button        ${TIMEOUT}

Test Everything
  [Tags]    auto
  Log To Console              Click Everything
  ${start}=   Get Time        epoch
  Click Element               id:fetch-button
  Log To Console              Click!
  Click Element               id:shorttimeout-button
  Log To Console              Click!
  Click Element               id:xhr-button
  Log To Console              Click!
  Click Element               id:transition-button
  Log To Console              Click!
  Click Element               id:animate-button
  Log To Console              Click!
  Wait For Testability Ready
  ${end}=   Get Time        epoch
  ${diff}=  Subtract Date From Date   ${end}  ${start}
  Should Be True              ${diff} >= 4.0
  

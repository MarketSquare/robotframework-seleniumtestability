*** Settings ***
Library         SeleniumLibrary   plugins=${CURDIR}/../src/SeleniumTestability;True;29 seconds;False
Library         Process
Library         Collections
Test Teardown   Teardown Test Environment
Test Template   Test Get Log
*** Variables ***
${URL}                  http://127.0.0.1:5000/
${FF}                   Headless Firefox
${CC}                   Headless Chrome

*** Test Cases ***
Logs With Firefox       ${FF}   loggingPrefs        0
Logs With Chrome        ${CC}   goog:loggingPrefs   10


*** Keywords ***
Start Flask App
  ${FLASK_HANDLE}=            Start Process   flask   run   shell=True    cwd=${CURDIR}/../assets
  Set Suite Variable          ${FH}   ${FLASK_HANDLE}

Stop Flask App
  Terminate Process           ${FH}   kill=True

Teardown Test Environment
  Stop Flask App
  Close All Browsers

Setup Test Environment
  [Arguments]                 ${BROWSER}    ${PREFS}   ${ROWS}
  Start Flask App
  ${defaults}=   Get Default Capabilities    ${BROWSER}
  ${browser_all}=     Create Dictionary    browser=ALL
  ${logging}=         Create Dictionary     ${PREFS}   ${browser_all}
  ${cap}=             Create Dictionary     &{defaults}   &{logging}
  Open Browser                ${URL}    browser=${BROWSER}   desired_capabilities=${cap}
  Wait For Document Ready
  FOR  ${idx}   IN RANGE  ${ROWS}
      Execute Javascript    console.log("Hello World ${idx}")
  END

Test Get Log
  [Arguments]                 ${BROWSER}  ${PREFS}   ${ROWS}
  Setup Test Environment      ${BROWSER}  ${PREFS}   ${ROWS}
  ${LOG}=                     Get Log   browser
  Length Should Be    ${LOG}    ${ROWS}
  Log To Console    ${LOG}    ${ROWS}

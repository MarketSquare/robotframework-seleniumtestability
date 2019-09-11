*** Settings ***
Documentation   Verifies log fetching
Suite Setup     Start Flask App
Suite Teardown  Stop Flask App
Test Teardown   Teardown Web Environment
Test Template   Test Get Log
Library         SeleniumLibrary  plugins=${CURDIR}/../src/SeleniumTestability;True;29 seconds;False
Resource        keywords.robot
Library         Collections

*** Test Cases ***
Logs With Firefox
  ${FF}  loggingPrefs  0

Logs With Chrome
  ${GC}  goog:loggingPrefs  10

*** Keywords ***
Local Setup Test Environment
  [Arguments]  ${BROWSER}  ${PREFS}  ${ROWS}
  [Documentation]  normal test setup but with desired_capabilities added
  ${cap}=  Generate Capabilities with Logging Prefs  ${BROWSER}  ${PREFS}
  Open Browser  ${URL}  browser=${BROWSER}  desired_capabilities=${cap}
  Wait For Document Ready
  FOR  ${idx}  IN RANGE  ${ROWS}
    Execute Javascript  console.log("Hello World ${idx}")
  END

Test Get Log
  [Arguments]  ${BROWSER}  ${PREFS}  ${ROWS}
  [Documentation]  Verifies get_log returns something when possible and doesnt cause errors
  Local Setup Test Environment  ${BROWSER}  ${PREFS}  ${ROWS}
  ${LOG}=  Get Log  browser
  Length Should Be  ${LOG}  ${ROWS}

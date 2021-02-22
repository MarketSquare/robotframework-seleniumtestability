*** Settings ***
Documentation   Verifies log fetching
Suite Setup     Start Flask App
Suite Teardown  Stop Flask App
Test Template   Test Get Log
Test Teardown   Teardown Web Environment
Library         SeleniumLibrary  plugins=${CURDIR}/../src/SeleniumTestability;True;29 seconds;False
Resource        resources.robot
Library         Collections

*** Test Cases ***
Logs With Firefox
  ${FF}   loggingPrefs  2  9  11

Logs With Chrome
  ${GC}   goog:loggingPrefs  2  5  10

*** Keywords ***
Local Setup Test Environment
  [Arguments]  ${BROWSER}  ${PREFS}
  [Documentation]  normal test setup but with desired_capabilities added
  ${cap}=  Generate Capabilities with Logging Prefs  ${BROWSER}  ${PREFS}
  ${FF_PROFILE}=     Generate Firefox Profile
  Open Browser  ${URL}  browser=${BROWSER}  desired_capabilities=${cap}  ff_profile_dir=${FF_PROFILE.path}
  Wait For Document Ready

Test Get Log
  [Arguments]  ${BROWSER}  ${PREFS}  ${ROWS}  ${FIRST}  ${SECOND}
  [Documentation]  Verifies get_log returns something when possible and doesnt cause errors.
  Local Setup Test Environment  ${BROWSER}  ${PREFS}
  Click Button    id:log-button
  ${LOG}=  Get Log  browser
  Length Should Be  ${LOG}  ${FIRST}
  FOR  ${idx}  IN RANGE  ${ROWS}
    Execute Javascript  console.log("Hello World ${idx}")
    Execute Javascript  console.info("Hello World ${idx} as info")
    Execute Javascript  console.warn("Hello World ${idx} as warn")
    Execute Javascript  console.error("Hello World ${idx} as error")
    Execute Javascript  console.trace("Hello World ${idx} as trace")
    Execute Javascript  console.debug("Hello World ${idx} as debug")
  END
  ${LOG}=  Get Log  browser
  Length Should Be  ${LOG}  ${SECOND}

*** Settings ***
Documentation   Verifies manual injection & waiting features
Suite Setup     Start Flask App
Suite Teardown  Internal Suite Teardown
Test Template   Manual Wait For Testability Ready
Library         SeleniumLibrary  plugins=${CURDIR}/../src/SeleniumTestability;False;30 seconds;True
Library         Timer
Resource        keywords.robot

*** Test Cases ***
Verify Fetch In Firefox
  ${FF}  fetch-button

Verify Timeout In Firefox
  ${FF}  shorttimeout-button

Verify XHR In Firefox
  ${FF}  xhr-button

Verify CSS Transition In Firefox
  ${FF}  transition-button

Verify CSS Animation In Firefox
  ${FF}  animate-button

Verify Fetch In Chrome
  ${GC}  fetch-button

Verify Timeout In Chrome
  ${GC}  shorttimeout-button

Verify XHR In Chrome
  ${GC}  xhr-button

Verify CSS Transition In Chrome
  ${GC}  transition-button

Verify CSS Animation In Chrome
  ${GC}  animate-button

*** Keywords ***
Add Final Benchmark Table
  [Documentation]  Verifies that all timers done during the suite are passing
  Verify All Timers  fail_on_errors=False

Manual Wait For Testability Ready
  [Arguments]  ${BROWSER}  ${ID}
  [Documentation]  test template for manual waiting & injection tests
  Setup Web Environment   ${BROWSER}    ${URL}
  Start Timer  ${TEST NAME}
  Click And Wait  ${ID}
  Stop Timer  ${TEST NAME}
  Verify Single Timer  5 seconds  3.5 seconds  ${TEST NAME}
  [Teardown]  Teardown Web Environment

Click And Wait
  [Arguments]  ${id}
  [Documentation]  Clicks element and manually waits for testability.
  Click Element  id:${id}
  Wait For Testability Ready  error_on_timeout=YES

Internal Suite Teardown
  [Documentation]  Final teardown
  Add Final Benchmark Table
  Teardown Test Environment

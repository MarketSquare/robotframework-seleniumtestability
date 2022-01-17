*** Settings ***
Documentation   Verifies manual injection & waiting features
Suite Setup     Start Flask App
Suite Teardown  Internal Suite Teardown
Test Template   Manual Wait For Testability Ready
Library         SeleniumLibrary  plugins=${CURDIR}/../src/SeleniumTestability;False;30 seconds;True
Library         Timer
Resource        resources.robot

*** Test Cases ***
Verify Fetch In Firefox
  ${FF}  fetch-button  3.5  4.5

Verify Timeout In Firefox
  ${FF}  shorttimeout-button  3.5  4.5

Verify XHR In Firefox
  ${FF}  xhr-button  3.5  4.5

Verify CSS Transition In Firefox
  ${FF}  transition-button  3.5  4.5

Verify CSS Animation In Firefox
  ${FF}  animate-button  3.5  4.5

Verify Fetch In Chrome
  ${GC}  fetch-button  3.5  4.5

Verify Timeout In Chrome
  ${GC}  shorttimeout-button  3.5  4.5

Verify XHR In Chrome
  ${GC}  xhr-button  3.5  4.5

Verify CSS Transition In Chrome
  ${GC}  transition-button  3.5  4.5

Verify CSS Animation In Chrome
  ${GC}  animate-button  3.5  4.5

*** Keywords ***
Add Final Benchmark Table
  [Documentation]  Verifies that all timers done during the suite are passing
  Verify All Timers  fail_on_errors=False

Internal Suite Teardown
  [Documentation]  Final teardown
  Add Final Benchmark Table
  Teardown Test Environment
  Remove All Timers

Manual Wait For Testability Ready
  [Arguments]  ${BROWSER}  ${ID}  ${HIGHER_THAN}  ${LOWER_THAN}
  [Documentation]  test template for manual waiting & injection tests
  Setup Web Environment   ${BROWSER}    ${URL}
  Start Timer  ${TEST NAME}-onClick
  Click Element  id:${id}
  Stop Timer  ${TEST NAME}-onClick
  Start Timer  ${TEST NAME}-onWait
  Wait For Testability Ready
  Stop Timer  ${TEST NAME}-onWait
  Verify Single Timer  ${LOWER_THAN}  ${HIGHER_THAN}  ${TEST NAME}-onWait
  Verify Single Timer  0.5  0  ${TEST NAME}-onClick
  [Teardown]  Teardown Web Environment

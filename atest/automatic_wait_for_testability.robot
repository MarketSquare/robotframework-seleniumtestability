*** Settings ***
Documentation   Verifies automatic injection & waiting features
Suite Setup     Start Flask App
Suite Teardown  Internal Suite Teardown
#Suite Teardown  Final Report
Test Template   Automatically Call Testability Ready Extra Check
Library         SeleniumLibrary  plugins=${CURDIR}/../src/SeleniumTestability;True;60 seconds;False
Library         Timer
Resource        resources.robot

*** Test Cases ***
Verify Fetch In Firefox
  ${FF}  fetch  not executed  executed at least once  3.5  4.5

Verify Timeout In Firefox
  ${FF}  shorttimeout  not executed  executed at least once  3.5  4.5

Verify XHR In Firefox
  ${FF}  xhr  not executed  executed at least once  3.5  4.5

Verify CSS Transition In Firefox
  ${FF}  transition  not executed  executed at least once  3.5  4.5

Verify CSS Animation In Firefox
  ${FF}  animate  not executed  executed at least once  3.5  4.5

Verify Fetch In Chrome
  ${GC}  fetch  not executed  executed at least once  3.5  4.5

Verify Timeout In Chrome
  ${GC}  shorttimeout  not executed  executed at least once  3.5  4.5

Verify XHR In Chrome
  ${GC}  xhr  not executed  executed at least once  3.5  4.5

Verify CSS Transition In Chrome
  ${GC}  transition  not executed  executed at least once  3.5  4.5

Verify CSS Animation In Chrome
  ${GC}  animate  not executed  executed at least once  3.5  4.5

*** Keywords ***
Add Final Benchmark Table
  [Documentation]  Verifies that all timers done during the suite are passing
  Verify All Timers  fail_on_errors=False

Internal Suite Teardown
  [Documentation]  Final teardown
  Add Final Benchmark Table
  Teardown Test Environment
  Remove All Timers

Automatically Call Testability Ready Extra Check
  [Arguments]  ${BROWSER}  ${ID}  ${PRE_MESSAGE}  ${POST_MESSAGE}  ${HIGHER_THAN}  ${LOWER_THAN}
  [Documentation]  test template for manual waiting & injection tests
  Setup Web Environment   ${BROWSER}    ${URL}
  Element Text Should Be  id:${id}-result  ${PRE_MESSAGE}
  Start Timer  ${TEST NAME}-onClick
  Click Element  id:${id}-button
  Stop Timer  ${TEST NAME}-onClick
  Start Timer  ${TEST NAME}-onGetText
  Element Text Should Be  id:${id}-result  ${POST_MESSAGE}
  Stop Timer  ${TEST NAME}-onGetText
  Start Timer  ${TEST NAME}-onWait
  Wait For Testability Ready
  Stop Timer  ${TEST NAME}-onWait
  Verify Single Timer  0.5  0  ${TEST NAME}-onClick
  Verify Single Timer  ${LOWER_THAN}  ${HIGHER_THAN}  ${TEST NAME}-onGetText
  Verify Single Timer  0.5  0  ${TEST NAME}-onWait
  [Teardown]  Teardown Web Environment

# Final Report
#   [Documentation]  Verifies that all timers done during the suite are passing
#   Stop Flask App
#   Verify All Timers  fail_on_errors=False
#   Remove All Timers

# Automatically Call Testability Ready
#   [Arguments]  ${BROWSER}  ${HIGHER_THAN}  ${LOWER_THAN}
#   [Documentation]  test template for automatic waiting and injection

#   &{longfetch}=   Create Dictionary   url=.*longfetch.*    method=GET
#   @{blacklist}=   Create List         ${longfetch}
#   ${tc}=          Create Dictionary   maxTimeout=5000    blacklist=${blacklist}
#   Set Testability Config    ${tc}

#   Setup Web Environment  ${BROWSER}  ${URL}
#   Click All And Verify  ${HIGHER_THAN}  ${LOWER_THAN}
#   [Teardown]  Teardown Web Environment

# Click All And Verify
#   [Arguments]  ${HIGHER_THAN}  ${LOWER_THAN}
#   [Documentation]  Click and verify enough time is passing
#   Start Timer  ${TEST NAME}
#   Click Element  id:fetch-button
#   Click Element  id:shorttimeout-button
#   Click Element  id:xhr-button
#   Click Element  id:transition-button
#   Click Element  id:animate-button
#   Wait For Testability Ready
#   Stop Timer  ${TEST NAME}
#   Verify Single Timer  ${LOWER_THAN}  ${HIGHER_THAN}  ${TEST NAME}
#   ${TIMEOUT}=   Get Selenium Timeout
#   Should Be Equal   ${TIMEOUT}  2 seconds

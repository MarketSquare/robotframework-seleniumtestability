*** Settings ***
Documentation   Verifies automatic injection & waiting features
Suite Setup     Start Flask App
Suite Teardown  Final Report
Test Template   Automatically Call Testability Ready
Library         SeleniumLibrary  plugins=${CURDIR}/../src/SeleniumTestability;True;29 seconds;False
Library         Timer
Resource        resources.robot

*** Test Cases ***
Testability in Firefox
  ${FF}  20 seconds  30 seconds

Testability in Chrome
  ${GC}  20 seconds  30 seconds

*** Keywords ***
Final Report
  [Documentation]  Verifies that all timers done during the suite are passing
  Stop Flask App
  Verify All Timers  fail_on_errors=False

Automatically Call Testability Ready
  [Arguments]  ${BROWSER}  ${HIGHER_THAN}  ${LOWER_THAN}
  [Documentation]  test template for automatic waiting and injection
  Setup Web Environment  ${BROWSER}  ${URL}
  Click All And Verify  ${HIGHER_THAN}  ${LOWER_THAN}
  [Teardown]  Teardown Web Environment

Click All And Verify
  [Arguments]  ${HIGHER_THAN}  ${LOWER_THAN}
  [Documentation]  Click and verify enough time is passing
  Start Timer  ${TEST NAME}
  Click Element  id:fetch-button
  Click Element  id:shorttimeout-button
  Click Element  id:xhr-button
  Click Element  id:transition-button
  Click Element  id:animate-button
  Wait For Testability Ready
  Stop Timer  ${TEST NAME}
  Verify Single Timer  ${LOWER_THAN}  ${HIGHER_THAN}  ${TEST NAME}

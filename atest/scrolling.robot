*** Settings ***
Documentation   Verifies that scrolling can trigger testability waits.
...             Disabled in CI because timings ci will vary a lot.
...             So these are only used locally.
Suite Setup     Local Suite Setup
Suite Teardown  Internal Suite Teardown
Test Template   Scrolling Up And Down
Force Tags      skipci
Library         SeleniumLibrary  plugins=${CURDIR}/../src/SeleniumTestability;False;29 seconds;False
Library         Timer
Resource        resources.robot


*** Variables ***
${URL}          http://127.0.0.1:5000/scroll

*** Test Cases ***
Scrolling In Firefox
  ${FF}

Scrolling In Chrome
  ${GC}

*** Keywords ***
Local Suite Setup
  [Documentation]   Firefox smooth scrolling is still really fast compared to chrome.
  ...               So its got still rather low "low" value in the timer..
  Start Flask App
  Remove All Timers
  Configure Timer   0.5 seconds   0 seconds     Scrolling In Firefox-INSTANT
  Configure Timer   5 seconds     0.1 seconds   Scrolling In Firefox-SMOOTH
  Configure Timer   0.5 seconds   0 seconds     Scrolling In Chrome-INSTANT
  Configure Timer   5 seconds     0.5 seconds   Scrolling In Chrome-SMOOTH


Add Final Benchmark Table
  [Documentation]  Verifies that all timers done during the suite are passing
  Verify All Timers  fail_on_errors=True

Scrolling Up And Down
  [Arguments]  ${BROWSER}
  [Documentation]  test template for manual waiting & injection tests
  Setup Web Environment   ${BROWSER}    ${URL}

  Start Timer   ${TEST NAME}-INSTANT
  Element Should Be Visible  //div[@class="top"]
  Scroll To Bottom    ${False}
  Wait For Testability Ready
  Stop Timer  ${TEST NAME}-INSTANT

  Start Timer  ${TEST NAME}-SMOOTH
  Element Should Be Visible  //div[@class="bottom"]
  Scroll To Top       ${True}
  Wait For Testability Ready
  Stop Timer  ${TEST NAME}-SMOOTH
  Element Should Be Visible  //div[@class="top"]

  [Teardown]  Teardown Web Environment

Internal Suite Teardown
  [Documentation]  Final teardown
  Add Final Benchmark Table
  Teardown Test Environment

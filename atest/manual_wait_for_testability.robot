*** Settings ***
Library         SeleniumLibrary   plugins=${CURDIR}/../src/SeleniumTestability;False;30 seconds;True
Library         Timer
Library         Process
Test Template   Manual Wait For Testability Ready
Suite Teardown  Add Final Benchmark Table

*** Variables ***
${URL}                  http://localhost:5000
${FF}                   Headless Firefox
${GC}                   Headless Chrome

*** Test Cases ***
Verify Fetch In Firefox             ${FF}   fetch-button
Verify Timeout In Firefox           ${FF}   shorttimeout-button
Verify XHR In Firefox               ${FF}   xhr-button
Verify CSS Transition In Firefox    ${FF}   transition-button
Verify CSS Animation In Firefox     ${FF}   animate-button

Verify Fetch In Chrome              ${GC}   fetch-button
Verify Timeout In Chrome            ${GC}   shorttimeout-button
Verify XHR In Chrome                ${GC}   xhr-button
Verify CSS Transition In Chrome     ${GC}   transition-button
Verify CSS Animation In Chrome      ${GC}   animate-button


*** Keywords ***
Add Final Benchmark Table
  Verify All Timers   fail_on_errors=False

Manual Wait For Testability Ready
  [Arguments]   ${BROWSER}    ${ID}
  [Teardown]    Teardown Test Environment
  Setup Test Environment    ${BROWSER}
  Start Timer               ${TEST NAME}
  Click And Wait            ${ID}
  Stop Timer                ${TEST NAME}
  Verify Single Timer       5 seconds   3.5 seconds   ${TEST NAME}


Start Flask App
  ${FLASK_HANDLE}=            Start Process   flask   run   shell=True    cwd=${EXEC_DIR}/assets
  Set Suite Variable        ${FH}   ${FLASK_HANDLE}

Stop Flask App
  Terminate Process           ${FH}   kill=True

Setup Test Environment
  [Arguments]   ${BROWSER}
  Start Flask App
  ${URL}=   Set Variable    ${URL}
  Set Selenium Timeout        120 seconds
  Open Browser                ${URL}    browser=${BROWSER}
  Wait For Document Ready

Teardown Test Environment
  Close Browser
  Stop Flask App

Click And Wait
  [Arguments]   ${id}
  Click Element               id:${id}
  Wait For Testability Ready    error_on_timeout=YES

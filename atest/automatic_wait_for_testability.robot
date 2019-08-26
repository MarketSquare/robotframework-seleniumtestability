*** Settings ***
Library         SeleniumLibrary   plugins=${CURDIR}/../src/SeleniumTestability;True;29 seconds;False
Library         Timer
Library         Process
Test Template   Automatically Call Testability Ready
Suite Teardown  Final Report

*** Variables ***
${URL}                  http://localhost:5000
${FF}                   Headless Firefox
${GC}                   Headless Chrome

*** Test Cases ***
Testability in Firefox  ${FF}   20 seconds   30 seconds
Testability in Chrome   ${GC}   20 seconds   30 seconds


*** Keywords ***
Final Report
  Verify All Timers   fail_on_errors=False

Automatically Call Testability Ready
  [Arguments]   ${BROWSER}    ${HIGHER_THAN}  ${LOWER_THAN}
  [Teardown]    Teardown Test Environment
  Setup Test Environment      ${BROWSER}
  Click All And Verify        ${HIGHER_THAN}  ${LOWER_THAN}

Click All And Verify
  [Arguments]   ${HIGHER_THAN}  ${LOWER_THAN}
  Start Timer                 ${TEST NAME}
  Click Element               id:fetch-button
  Click Element               id:shorttimeout-button
  Click Element               id:xhr-button
  Click Element               id:transition-button
  Click Element               id:animate-button
  Wait For Testability Ready
  Stop Timer                   ${TEST NAME}
  Verify Single Timer         ${LOWER_THAN}   ${HIGHER_THAN}  ${TEST NAME}


Start Flask App
  ${FLASK_HANDLE}=            Start Process   flask   run   shell=True    cwd=${CURDIR}/../assets
  Set Suite Variable          ${FH}   ${FLASK_HANDLE}

Stop Flask App
  Terminate Process           ${FH}   kill=True

Setup Test Environment
  [Arguments]   ${BROWSER}
  Start Flask App
  ${URL}=   Set Variable      ${URL}
  Set Selenium Timeout        120 seconds
  Open Browser                ${URL}    browser=${BROWSER}
  Wait For Document Ready

Teardown Test Environment
  Close Browser
  Stop Flask App

Library         SeleniumLibrary   plugins=${CURDIR}/../src/SeleniumTestability;True;29 seconds;False
Library         SeleniumLibrary   plugins=${CURDIR}/../src/SeleniumTestability;True;29 seconds;False
*** Settings ***
Library         SeleniumLibrary   plugins=${CURDIR}/../src/SeleniumTestability;False;30 seconds;True
Library         DateTime
Library         Process
Test Template   Manual Wait For Testability Ready

*** Variables ***
${URL}                  http://localhost:5000
${FF}                   Headless Firefox
${GC}                   Headless Chrome

*** Test Cases ***
Verify Fetch In Firefox             ${FF}   4.0   fetch-button
Verify Timeout In Firefox           ${FF}   4.0   shorttimeout-button
Verify XHR In Firefox               ${FF}   4.0   xhr-button
Verify CSS Transition In Firefox    ${FF}   4.0   transition-button
Verify CSS Animation In Firefox     ${FF}   4.0   animate-button

Verify Fetch In Chrome              ${GC}   4.0   fetch-button
Verify Timeout In Chrome            ${GC}   4.0   shorttimeout-button
Verify XHR In Chrome                ${GC}   4.0   xhr-button
Verify CSS Transition In Chrome     ${GC}   4.0   transition-button
Verify CSS Animation In Chrome      ${GC}   4.0   animate-button


*** Keywords ***
Manual Wait For Testability Ready
  [Arguments]   ${BROWSER}    ${TIMEOUT}  ${ID}
  [Teardown]    Teardown Test Environment

  Setup Test Environment    ${BROWSER}
  Click And Verify    ${ID}   ${TIMEOUT}


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

Click And Verify
  [Arguments]   ${id}    ${duration}
  ${start}=   Get Time        epoch
  Click Element               id:${id}
  Wait For Testability Ready
  ${end}=   Get Time        epoch
  ${diff}=  Subtract Date From Date   ${end}  ${start}
  Should Be True              not ${diff} < ${duration}

*** Settings ***
Library         ${CURDIR}/../src/SeleniumTestability       wait_testability=False
Library         DateTime
Library         Process
Test Template   Manual Wait For Testability Ready

*** Variables ***
${URL}                  http://localhost:5000
${INJECT_FROM_RF}       0

*** Test Cases ***
Verify Fetch In Firefox             Firefox   4.0   fetch-button
Verify Timeout In Firefox           Firefox   4.0   shorttimeout-button
Verify XHR In Firefox               Firefox   4.0   xhr-button
Verify CSS Transition In Firefox    Firefox   4.0   transition-button
Verify CSS Animation In Firefox     Firefox   4.0   animate-button

Verify Fetch In Chrome              Chrome    4.0   fetch-button
Verify Timeout In Chrome            Chrome    4.0   shorttimeout-button
Verify XHR In Chrome                Chrome    4.0   xhr-button
Verify CSS Transition In Chrome     Chrome    4.0   transition-button
Verify CSS Animation In Chrome      Chrome    4.0   animate-button


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
  ${URL}=   Set Variable    ${URL}?inject=${INJECT_FROM_RF}
  Set Selenium Timeout        120 seconds
  Open Browser                ${URL}    browser=${BROWSER}
  Run Keyword If    ${INJECT_FROM_RF}==1   Inject Testability
  Instrument Browser
  Wait For Document Ready

Teardown Test Environment
  Restore Run Keyword
  Stop Flask App
  Close Browser

Click And Verify
  [Arguments]   ${id}    ${duration}
  ${start}=   Get Time        epoch
  Click Element               id:${id}
  Wait For Testability Ready
  ${end}=   Get Time        epoch
  ${diff}=  Subtract Date From Date   ${end}  ${start}
  Should Be True              not ${diff} < ${duration}

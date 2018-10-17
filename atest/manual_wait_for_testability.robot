*** Settings ***
Library         SeleniumTestability     wait_on_run_keyword=False
Library         DateTime
Library         Process
Test Template   Manual Wait For Testability Ready

*** Variables ***
${URL}                  http://localhost:5000
${INJECT_FROM_RF}       0
${FLASK_HANDLE}         None

*** Test Cases ***
Verify Fetch            Firefox   4.0   fetch-button
Verify Timeout          Firefox   4.0   shorttimeout-button
Verify XHR              Firefox   4.0   xhr-button
Verify CSS Transition   Firefox   4.0   transition-button
Verify CSS Animation    Firefox   4.0   animate-button

*** Keywords ***
Manual Wait For Testability Ready
  [Arguments]   ${BROWSER}    ${TIMEOUT}  ${ID}
  [Teardown]    Teardown Test Environment

  Setup Test Environment    ${BROWSER}
  Click And Verify    ${ID}   ${TIMEOUT}


Start Flask App
  ${FLASK_HANDLE}=            Start Process   flask   run   shell=True    cwd=${EXEC_DIR}/assets

Stop Flask App
  Terminate Process           ${FLASK_HANDLE}   kill=True

Setup Test Environment
  [Arguments]   ${BROWSER}
  Start Flask App
  ${URL}=   Set Variable    ${URL}?inject=${INJECT_FROM_RF}
  Set Selenium Timeout        120 seconds
  Open Browser                ${URL}    browser=${BROWSER}
  Run Keyword If    ${INJECT_FROM_RF}==1   Inject Testability
  Instrument Browser

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

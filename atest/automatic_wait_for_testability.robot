*** Settings ***
Library         SeleniumTestability
Library         DateTime
Library         Process
Test Template   Automatically Call Testability Ready

*** Variables ***
${URL}                  http://localhost:5000
${INJECT_FROM_RF}       0
${FLASK_HANDLE}         None

*** Test Cases ***
Patched Run Keywords    Firefox   20.0   30.0   True
Unpatched Run Keywords  Firefox   4.0    5.0    False


*** Keywords ***
Automatically Call Testability Ready
  [Arguments]   ${BROWSER}    ${HIGHER_THAN}  ${LOWER_THAN}   ${PATCH_RUN_KEYWORD}
  [Teardown]    Teardown Test Environment

  Setup Test Environment    ${BROWSER}  ${PATCH_RUN_KEYWORD}
  Click All And Verify    ${HIGHER_THAN}  ${LOWER_THAN}

Click All And Verify
  [Arguments]   ${HIGHER_THAN}  ${LOWER_THAN}
  ${start}=   Get Time        epoch
  Click Element               id:fetch-button
  Click Element               id:shorttimeout-button
  Click Element               id:xhr-button
  Click Element               id:transition-button
  Click Element               id:animate-button
  Wait For Testability Ready
  ${end}=   Get Time        epoch
  ${diff}=  Subtract Date From Date   ${end}  ${start}
  Should Be True              ${diff} >= ${HIGHER_THAN}
  Should Be True              ${diff} <= ${LOWER_THAN}


Start Flask App
  ${FLASK_HANDLE}=            Start Process   flask   run   shell=True    cwd=${EXEC_DIR}/assets

Stop Flask App
  Terminate Process           ${FLASK_HANDLE}   kill=True

Setup Test Environment
  [Arguments]   ${BROWSER}    ${PATCH}
  Start Flask App
  ${URL}=   Set Variable    ${URL}?inject=${INJECT_FROM_RF}
  Set Selenium Timeout        120 seconds
  Open Browser                ${URL}    browser=${BROWSER}
  Instrument Browser
  Run Keyword If    ${PATCH}==True   Patch Run Keyword

Teardown Test Environment
  Restore Run Keyword
  Stop Flask App
  Close Browser

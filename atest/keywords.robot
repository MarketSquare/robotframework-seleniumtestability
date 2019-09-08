*** Settings ***
Documentation   Helper keywords and variables
Library         Process

*** Variables ***
${URL}          http://localhost:5000
${FF}           Headless Firefox
${GC}           Headless Chrome

*** Keywords ***
Teardown Web Environment
  [Documentation]  Closes all browsers
  Close All Browsers

Setup Web Environment
  [Arguments]  ${BROWSER}  ${URL}
  [Documentation]  Opens a browser witth given url
  ${URL}=  Set Variable  ${URL}
  Set Selenium Timeout  120 seconds
  Open Browser  ${URL}  browser=${BROWSER}
  Wait For Document Ready

Start Flask App
  [Documentation]  Starts flask
  ${FLASK_HANDLE}=  Start Process  flask  run  shell=True  cwd=${CURDIR}/../assets
  Set Suite Variable  ${FH}  ${FLASK_HANDLE}

Stop Flask App
  [Documentation]  Stops flask
  Terminate Process  ${FH}  kill=True

Setup Test Environment
  [Arguments]  ${BROWSER}  ${URL}
  [Documentation]  Starts flask and opens a browser
  Start Flask App
  Setup Web Environment  ${BROWSER}  ${URL}

Teardown Test Environment
  [Documentation]  Stops flask and closes all browsers
  Teardown Web Environment
  Stop Flask App

*** Settings ***
Documentation   Helper keywords and variables
Library         Process
Library         Helpers

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
  [Documentation]  Opens a browser with given url
  ${URL}=  Set Variable  ${URL}
  ${FF_PROFILE}=     Generate Firefox Profile
  Set Selenium Speed  0 seconds
  Open Browser  ${URL}  browser=${BROWSER}      ff_profile_dir=${FF_PROFILE.path}
  Wait For Document Ready

Start Flask App
  [Documentation]  Starts flask
  ${FH}=  Start Process  python  -mflask  run  shell=True  cwd=${CURDIR}/../assets  stdout=stdout.txt  stderr=stderr.txt
  Set Suite Variable  ${FLASK_HANDLE}  ${FH}

Stop Flask App
  [Documentation]  Stops flask
  ${pid}=   Get Process Id    ${FLASK_HANDLE}
  Die Die Die   ${pid}

Setup Test Environment
  [Arguments]  ${BROWSER}  ${URL}
  [Documentation]  Starts flask and opens a browser
  Start Flask App
  Setup Web Environment  ${BROWSER}  ${URL}

Teardown Test Environment
  [Documentation]  Stops flask and closes all browsers
  Teardown Web Environment
  Stop Flask App


Generate Capabilities with Logging Prefs
  [Documentation]  Generates default_capabilities with browser all to given loging prefs
  [Arguments]   ${BROWSER}  ${PREFNAME}
  ${defaults}=  Get Default Capabilities  ${BROWSER}
  ${browser_all}=  Create Dictionary  browser=ALL
  ${logging}=  Create Dictionary  ${PREFNAME}  ${browser_all}
  ${cap}=  Create Dictionary  &{defaults}  &{logging}
  [return]  ${cap}

*** Settings ***
Library         SeleniumLibrary   plugins=${CURDIR}/../src/SeleniumTestability;True;29 seconds;False
Library         Process
Test Setup      Setup Test Environment
Test Teardown   Teardown Test Environment

*** Variables ***
${URL}                  http://127.0.0.1:5000/
${FF}                   Headless Firefox

*** Keywords ***
Teardown Test Environment
  Stop Flask App
  Close All Browsers

Setup Test Environment
  Start Flask App
  Set Selenium Timeout        120 seconds
  Open Browser                ${URL}    browser=${FF}
  Wait For Document Ready


Start Flask App
  ${FLASK_HANDLE}=            Start Process   flask   run   shell=True    cwd=${CURDIR}/../assets
  Set Suite Variable          ${FH}   ${FLASK_HANDLE}

Stop Flask App
  Terminate Process           ${FH}   kill=True

*** Test Cases ***
Drag And Drop Test
  Run Keyword And Expect Error    STARTS: Element with locator
  ...                             Get WebElement   xpath://*[@id="div1"]/img
  Drag And Drop   xpath://*[@id="drag1"]    xpath://*[@id="div1"]   html5=True
  Get WebElement   xpath://*[@id="div1"]/img

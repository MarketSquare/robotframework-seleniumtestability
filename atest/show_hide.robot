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
  Open Browser                ${URL}    browser=${FF}
  Wait For Document Ready

Start Flask App
  ${FLASK_HANDLE}=            Start Process   flask   run   shell=True    cwd=${CURDIR}/../assets
  Set Suite Variable          ${FH}   ${FLASK_HANDLE}

Stop Flask App
  Terminate Process           ${FH}   kill=True

*** Test Cases ***
Show And Hide Test
  Run Keyword And Expect Error    STARTS: ElementClickInterceptedException
  ...                             Click Button    id:hiddenbutton
  Element Should Be Blocked       id:hiddenbutton
  Hide Element                    id:infoi
  Element Should Not Be Blocked   id:hiddenbutton
  Click Button                    id:hiddenbutton
  Show Element                    id:infoi
  Element Should Be Blocked       id:hiddenbutton
  Run Keyword And Expect Error    STARTS: ElementClickInterceptedException
  ...                             Click Button    id:hiddenbutton
  Run Keyword And Expect Error    STARTS: Element with locator
  ...                             Element Should Not Be Blocked   id:hiddenbutton

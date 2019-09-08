*** Settings ***
Documentation   Verifies webelement show hide features.
Test Teardown   Tear Down Test Environment
Test Template   Show And Hide Test
Library         SeleniumLibrary  plugins=${CURDIR}/../src/SeleniumTestability;True;29 seconds;False
Resource        keywords.robot

*** Test Cases ***
Show And Hide In Firefox
  ${FF}  ${URL}

Show And Hide In Chrome
  ${GC}  ${URL}

*** Keywords ***
Show And Hide Test
  [Arguments]  ${BROWSER}  ${URL}
  [Documentation]  Hides and shows elements via different keywords
  Setup Test Environment  ${BROWSER}  ${URL}
  Run Keyword And Expect Error  STARTS: ElementClickInterceptedException  Click Button  id:hiddenbutton
  Element Should Be Blocked  id:hiddenbutton
  Hide Element  id:infoi
  Element Should Not Be Blocked  id:hiddenbutton
  Click Button  id:hiddenbutton
  Show Element  id:infoi
  Element Should Be Blocked  id:hiddenbutton
  Run Keyword And Expect Error  STARTS: ElementClickInterceptedException  Click Button  id:hiddenbutton
  Run Keyword And Expect Error  STARTS: Element with locator  Element Should Not Be Blocked  id:hiddenbutton

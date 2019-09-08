*** Settings ***
Documentation   Verifies that html5 dragndrop events work
Test Teardown   Tear Down Test Environment
Test Template   Drag And Drop Test
Library         SeleniumLibrary  plugins=${CURDIR}/../src/SeleniumTestability;True;29 seconds;False
Resource        keywords.robot

*** Test Cases ***
Drag And Drop in Firefox
  ${FF}  ${URL}

Drag And Drop in Chrome
  ${GC}  ${URL}

*** Keywords ***
Drag And Drop Test
  [Arguments]  ${BROWSER}  ${URL}
  [Documentation]  Drags and drops image from element to another
  Setup Test Environment  ${BROWSER}  ${URL}
  Run Keyword And Expect Error  STARTS: Element with locator  Get WebElement  xpath://*[@id="div1"]/img
  Drag And Drop  xpath://*[@id="drag1"]  xpath://*[@id="div1"]  html5=True
  Get WebElement  xpath://*[@id="div1"]/img

*** Settings ***
Documentation   Verifies right click alias
Suite Setup     Start Flask App
Suite Teardown  Stop Flask App
Test Teardown   Teardown Web Environment
Test Template   Test Right Click Alias
Library         SeleniumLibrary  plugins=${CURDIR}/../src/SeleniumTestability;True;29 seconds;False
Resource        resources.robot


*** Variables ***
${URL}      http://127.0.0.1:5000/context-menu
${BEFORE}   not executed
${AFTER}    executed at least once

*** Test Cases ***
Right Click With Firefox
  ${FF}

Right Click With Chrome
  ${GC}

*** Keywords ***
Test Right Click Alias
  [Arguments]  ${BROWSER}
  [Documentation]  Verifies Right Click Alias
  Setup Web Environment  ${BROWSER}  ${URL}

  ${val}=   Get Text  xpath://*[@id="contextmenu-result"]
  Should Be Equal   ${val}   ${BEFORE}

  Right Click Element   xpath://*[@id="contextmenu-trigger"]
  ${val}=   Get Text  xpath://*[@id="contextmenu-result"]
  Should Be Equal   ${val}   ${AFTER}


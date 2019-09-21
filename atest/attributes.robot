*** Settings ***
Documentation   Verifies webelement attribute getters/setters
Suite Setup     Start Flask App
Suite Teardown  Stop Flask App
Test Teardown   Teardown Web Environment
Test Template   Show And Hide Test
Library         SeleniumLibrary  plugins=${CURDIR}/../src/SeleniumTestability;True;29 seconds;False
Resource        resources.robot

*** Test Cases ***
Set Attribute In Firefox
  ${FF}  ${URL}

Set Attribute In Chrome
  ${GC}  ${URL}

*** Keywords ***
Show And Hide Test
  [Arguments]  ${BROWSER}  ${URL}
  [Documentation]  Verifies Set Element Attribute
  Setup Web Environment  ${BROWSER}  ${URL}
  ${x}=  Get Element Attribute  id:infoi  random_attribute
  Should Be Equal   ${x}  yey
  Set Element Attribute   id:infoi  random_attribute  NAY!
  ${x}=  Get Element Attribute  id:infoi    random_attribute
  Should Be Equal   ${x}  NAY!

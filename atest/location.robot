*** Settings ***
Documentation   Verifies location keywords
Suite Setup     Start Flask App
Suite Teardown  Stop Flask App
Test Teardown   Teardown Web Environment
Test Template   Test Cookies
Library         SeleniumLibrary  plugins=${CURDIR}/../src/SeleniumTestability;True;29 seconds;False
Resource        resources.robot
Library         Collections

*** Test Cases ***
Location With Firefox
  ${FF}

Location With Chrome
  ${GC}

*** Keywords ***
Test Cookies
  [Arguments]  ${BROWSER}
  [Documentation]  Verifies that location keywords return somewhat expected answers.
  Setup Web Environment  ${BROWSER}  ${URL}

  ${value}=    Get Location Hash
  Should Be Equal   ${value}   ${EMPTY}

  ${value}=    Get Location Host
  Should Be Equal   ${value}   localhost:5000

  ${value}=    Get Location Hostname
  Should Be Equal   ${value}   localhost

  ${value}=    Get Location HREF
  Should Be Equal   ${value}   ${URL}/

  ${value}=    Get Location Origin
  Should Be Equal   ${value}   ${URL}

  ${value}=    Get Location Port
  Should Be Equal   ${value}   5000

  ${value}=    Get Location Protocol
  Should Be Equal   ${value}   http:

  ${value}=    Get Location Search
  Should Be Equal   ${value}   ${EMPTY}

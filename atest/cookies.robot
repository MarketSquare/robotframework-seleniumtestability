*** Settings ***
Documentation   Verifies cookie keywords
Test Teardown   Teardown WEb Environment
Test Template   Test Cookies
Library         SeleniumLibrary  plugins=${CURDIR}/../src/SeleniumTestability;True;29 seconds;False
Resource        keywords.robot
Library         Collections

*** Variables ***
${URL}          http://www.google.com

*** Test Cases ***
Cookies With Firefox
  ${FF}

Cookies With Chrome
  ${GC}

*** Keywords ***
Test Cookies
  [Arguments]  ${BROWSER}
  [Documentation]  gets cookies and verifies everything is present
  Setup Web Environment  ${BROWSER}  ${URL}
  ${cookies}=  Get Cookies
  &{cookies_dict}=  Cookies To Dict  ${cookies}
  FOR  ${key}  IN  @{cookies_dict.keys()}
    ${value}=  Get From Dictionary  ${cookies_dict}  ${key}
    Should Contain  ${cookies}  ${key}=${value}
  END

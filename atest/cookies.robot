*** Settings ***
Library         SeleniumLibrary   plugins=${CURDIR}/../src/SeleniumTestability;True;29 seconds;False
Library         Process
Library         Collections
Test Teardown   Teardown Test Environment
Test Template   Test Cookies
*** Variables ***
${URL}                  http://www.google.com
${FF}                   Headless Firefox
${CC}                   Headless Chrome

*** Test Cases ***
Cookies With Firefox       ${FF}
Cookies With Chrome        ${CC}


*** Keywords ***
Teardown Test Environment
  Close All Browsers

Setup Test Environment
  [Arguments]                 ${BROWSER}
  Open Browser                ${URL}    browser=${BROWSER}
  Wait For Document Ready

Test Cookies
  [Arguments]                 ${BROWSER}
  Setup Test Environment      ${BROWSER}
  ${cookies}=                 Get Cookies
  &{cookies_dict}=            Cookies To Dict   ${cookies}

  FOR   ${key}    IN    @{cookies_dict.keys()}
      ${value}=         Get From Dictionary   ${cookies_dict}    ${key}
      Should Contain    ${cookies}            ${key}=${value}
  END

*** Settings ***
Documentation   Verifies that files can be dragged into browser
Test Teardown   Close All Browsers
Test Template   Dropzone Test
Library         SeleniumLibrary  plugins=${CURDIR}/../src/SeleniumTestability;False;29 seconds;False
Resource        resources.robot

*** Variables ***
${URL}    https://www.dropzonejs.com
${FILENAME}   resources.robot


*** Test Cases ***
Drag And Drop File in Firefox
  ${FF}   ${URL}

Drag And Drop File in Chrome
  ${GC}   ${URL}

*** Keywords ***
Dropzone Test
  [Arguments]   ${BROWSER}  ${URL}
  [Documentation]  Drags and drops image from element to another
  Setup Web Environment   ${BROWSER}    ${URL}
  Page Should Not Contain    xpath://div[@class="dz-filename"]
  Drag And Drop   file:${CURDIR}${/}${FILENAME}    xpath://div[contains(concat(' ',normalize-space(@class),' '),' dropzone ')]
  Element Should Contain    xpath://div[@class="dz-filename"]   ${FILENAME}

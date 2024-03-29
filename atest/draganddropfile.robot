*** Settings ***
Documentation   Verifies that files can be dragged into browser
Test Teardown   Close All Browsers
Test Template   Dropzone Test
Library         SeleniumLibrary  plugins=${CURDIR}/../src/SeleniumTestability;False;29 seconds;False
Force Tags      skipci
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
  Element Should Not Contain    xpath://div[@class="dropzone"]    ${FILENAME}
  Drag And Drop   file:${CURDIR}${/}${FILENAME}    id:demo-upload
  Element Should Contain    xpath://div[@class="dz-filename"]   ${FILENAME}

*** Settings ***
Documentation   Verifies url keywords
Library         SeleniumLibrary  plugins=${CURDIR}/../src/SeleniumTestability;True;29 seconds;False
Resource        resources.robot
Force Tags      skipci
Suite Setup     Start Flask App
Suite Teardown  Stop Flask App
Test Template   Open Browser With Auth
Test Teardown   Teardown Web Environment

*** Variables ***
${URL}          http://127.0.0.1:5000/secret
${SUBURL}       http://127.0.0.1:5000/secret/sub
${USER}         demo
${PASS}         mode

*** Test Cases ***
Auth With Firefox   ${FF}   ${URL}
Auth With Chrome    ${GC}   ${URL}
*** Keywords ***

Open Browser With Auth
  [Documentation]   Opens browser to basic auth site and does redirection
  [Arguments]   ${BROWSER}    ${URL}
  ${AUTH}=  Add Basic Authentication To Url  ${URL}  ${USER}  ${PASS}
  Setup Web Environment  ${BROWSER}   ${AUTH}
  Page Should Contain Element   id:redirect-button
  Click Button    id:redirect-button
  Page Should Contain Element   id:redirect-button
  Location Should Be    ${SUBURL}

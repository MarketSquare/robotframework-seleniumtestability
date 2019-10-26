*** Settings ***
Documentation   Verifies storage keywords
Test Teardown   Teardown Web Environment
Test Template   Test Storage 
Suite Setup     Start Flask App
Suite Teardown  Stop Flask App
Library         SeleniumLibrary  plugins=${CURDIR}/../src/SeleniumTestability;True;29 seconds;False
Resource        resources.robot
Library         Collections

*** Test Cases ***
Storage With Firefox
  ${FF}

Storage With Chrome
  ${GC}

*** Keywords ***
Test Storage
  [Arguments]  ${BROWSER}
  [Documentation]   interacts with session and localstorage
  Setup Web Environment  ${BROWSER}  ${URL}

  ${local}=     Get Storage Length
  Should Be Equal As Integers  ${local}    4
  ${session}=   Get Storage Length    storage_type=sessionStorage
  Should Be Equal As Integers  ${session}  4
  Clear Storage   storage_type=sessionStorage
  ${session}=   Get Storage Length    storage_type=sessionStorage
  Should Be Equal As Integers  ${session}  0

  ${storage_keys}=  Get Storage Keys    storage_type=localStorage
  FOR   ${key}  IN  @{storage_keys}
      ${value}=   Get Storage Item    ${key}    storage_type=localStorage
      Set Storage Item  ${key}    ${value}    storage_type=sessionStorage
      ${another_value}=   Get Storage Item    ${key}    storage_type=sessionStorage
      Should Be Equal   ${value}    ${another_value}
  END

  ${session}=   Get Storage Length    storage_type=sessionStorage
  Should Be Equal As Integers  ${session}  4

  ${storage_keys}=  Get Storage Keys    storage_type=sessionStorage
  FOR   ${key}  IN  @{storage_keys}
    Remove Storage Item   ${key}    storage_type=sessionStorage
  END
  
  ${session}=   Get Storage Length    storage_type=sessionStorage
  Should Be Equal As Integers  ${session}  0

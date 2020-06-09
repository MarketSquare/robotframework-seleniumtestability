*** Settings ***
Documentation   Verifies navigator keywords
Suite Setup     Start Flask App
Suite Teardown  Stop Flask App
Test Teardown   Teardown Web Environment
Test Template   Navigator Tests
Library         SeleniumLibrary  plugins=${CURDIR}/../src/SeleniumTestability;True;29 seconds;False
Resource        resources.robot

*** Test Cases ***
Navigator properties in Firefox
  ${FF}  ${URL}  Firefox

Navigator propreties in Chrome
  ${GC}  ${URL}  Chrome

*** Keywords ***
Navigator Tests
  [Arguments]  ${BROWSER}  ${URL}  ${UA}
  [Documentation]  Hides and shows elements via different keywords
  Setup Web Environment  ${BROWSER}  ${URL}


  ${user_agent}=    Get Navigator User Agent
  Should Contain    ${user_agent}   ${UA}

  ${appcode}=       Get Navigator AppCodeName
  Should Contain    ${appcode}    Mozilla

  ${appname}=       Get Navigator AppName
  Should Contain    ${appname}    Netscape

  ${appversion}=    Get Navigator AppVersion
  Should Contain    ${appversion}   5.0


  ${cenabled}=      Get Navigator CookieEnabled
  Should Be True    ${cenabled}

  ${language}=      Get Navigator Language
  Should Match Regexp   ${language}   ^(\\w{2}-\\w{2})$

  ${online}=        Get Navigator Online
  Should Be True    ${online}

  ${platform}=      Get Navigator Platform
  Should Not Be Empty   ${platform}

  ${product}=       Get Navigator Product
  Should Contain    ${product}    Gecko

*** Settings ***
Library         SeleniumLibrary
Library         ${CURDIR}/../src/SeleniumTestability     enable_implicit_wait=True

Suite Setup       Open Browser    http://www.google.com       browser=Firefox
Suite Teardown    Close Browser

Test Setup        Go To           http://www.google.com
*** Test Cases ***
Can Be Instrumented ?
    Instrument Browser
    ${result}=      Is Testability Installed
    Should Be True      ${result}

Not Instrumented
    ${result}=      Is Testability Installed
    Should Not Be True  ${result}


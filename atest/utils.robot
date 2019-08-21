*** Settings ***
Library         SeleniumLibrary   plugins=${CURDIR}/../src/SeleniumTestability;True;29 seconds;False

*** Variables ***
${URL}                  http://host/path/name.txt
${USER}                 foo
${PASS}                 bar

*** Test Cases ***
URL Splitting
    ${result}=    Split Url To Host And Path    ${URL}
    Should Be Equal   ${result['base']}  http://host
    Should Be Equal   ${result['path']}  /path/name.txt

Auth Mangling
    ${result}=    Add Basic Authentication To Url   ${URL}    ${USER}   ${PASS}
    Should Be Equal   ${result}   http://foo:bar@host/path/name.txt

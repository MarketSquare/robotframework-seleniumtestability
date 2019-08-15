*** Settings ***
#Library   SeleniumLibrary   plugins=SeleniumTestability   event_firing_webdriver=SeleniumTestability.TestabilityListener
Library   SeleniumLibrary   plugins=SeleniumTestability


*** Test Cases ***
Test
  Open Browser    http://www.pcuf.fi/~rasjani     browser=Firefox
  Sleep   3 seconds
  ${x}=   Testability Loaded
  Log To Console    RES: ${x}
  Inject Testability
  Sleep   3 seconds
  Instrument Browser
  ${x}=   Testability Loaded
  Log To Console    RES: ${x}
  Go To    https://www.google.com
  Sleep   1 seconds
  ${x}=   Testability Loaded
  Log To Console    RES: ${x}
  Close All Browsers

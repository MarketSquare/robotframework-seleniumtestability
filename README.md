robotframework-seleniumtestability
==================================

Extension plugin for Robot Framework's SeleniumLibrary >= 4.0.0 that provides
help with dealing asyncronous events by providing either automatic or manual
waits for the duration of real actions happening within SUT, not arbituary
length sleeps. There are also some helper functions which are out of scope
of upstream SeleniumLibrary but useful for testing web applications with it.

SeleniumTestability relies on core Selenium's feature Event Firing Webdriver
and provides it's own listener interface that takes care of waiting in right
places and instrumenting the SUT whenever it is needed.

Plugin also includes a a set of other functionality to ease the development in web enviroment.

# Project Dependencies

 * https://github.com/alfonso-presa/testability.js
 * https://github.com/alfonso-presa/testability-browser-bindings


# Installation

```
pip install robotframework-seleniumtestability
```

# Usage

## Initialize library

```
Library         SeleniumLibrary     plugins=SeleniumTestability;True;30 Seconds;True
```

## Parameters

`plugins=` part is standard SeleniumLibrary parameter where first part is
the plugin to load and rest of the string with semicolon separators are
parameters passed to the said plugin.

SeleniumTestabiluty has following parameters and in following order:

### automatic_wait

a truthy value, if SeleniumTestabily should automatically wait for sut to be in
state that it can accept more actions.

Can be enabled/disable at runtime.

Defaults to True

### timeout

Robot timestring, amount of time to wait for SUT to be in state that it can be
safely interacted with.

Can be set at runtime.

Defaults to 30 seconds.

### error_on_timeout

A truthy value, if timeout does occur either in manual or automatic mode, this
determines if error should be thrown that marks marks the exection as failure.

Can be enabled/disabled at runtime.

Defaults to True

### automatic_injection

A truthy value. User can choose if he wants to instrument the SUT manually with
appropriate keywords (or even, if the SUT is instrumented at build time?) or
should SeleniumTestability determinine if SUT has testability features and if not
then inject & instrument it automatically.

Can be enabled/disabled at runtime.

Defaults to True

## Example

```robotframework
  Click Element             id:button_that_triggers_ajax_request
  Click Element             id:some_other_element
  Log To Console            This will happen right after clicking
```

In here, if automatic_wait has been enabled, second `Click Element` keyword wont
be executed before action triggered by the first button is finished.

If automatic_wait is not enabled, test case can request the wait itself and previous
example would look something like this.

```
  Click Element               id:button_that_triggers_ajax_request
  Wait For Testability Ready
  Click Element               id:some_other_element
  Wait For Testability Ready
  Log To Console              This would show after events triggered by second click are done.
```

# Currently Supported Asyncronous features

* Can detect setTimeout & setImmediate calls and wait for them.
* Can detect fetch() call and wait for it to finish
* Can detect XHR requests and wait for them to finish
* Can detect CSS Animations and wait form them to finish
* Can detect CSS Transitions and wait form them to finish

Do note that CSS animations and transitions might not work in all browsers.
In the past, Chrome has been a bit lacking but at the moment, our acceptance
tests do show they work.

# Extra Keywords

* Add Basic Authentication To **URL   URL,   USER,   PASSWORD**

  * Takes in url, username and password and combines them together into single url that can be used for sites that use Basic Authentication.

* Split URL to Host and PATH **URL**

  * Takes in url and returns a dict  with keys base and path. Useful when constructing requests sessions.

* Cookies To Dict  **CookieString**

  * Takes a cookie string from the browser and converts it to dict. Useful when constructing requests sessions and one needs to provide authentication from existing selenium session.

* Get Current Useragent

  * Returns the useragent of the currently selected browser. Useful when constructing requests sessions.

* Drag And Drop   **From, To, HTML5**

  * Current implementation of Drag And Drop keyword in SeleniumLibrary does not work in all web application. Mainly because HTML5 events are not generated. If you set HTML5 to truthy value, the these events are generated and applications that rely on those drag&drop events should work properly.

* Scroll To Bottom / Scroll To Top

  * Conveniance functions  to set the browser viewport to top or bottom of the page.

* Toggle Element Visibility / Hide Element / Show Element  **Locator**

  * Toggles element on or off.  This is sometimes necessary when trying to interact with elements that are blocked via other elements on higher Z index. Combine this with *Is Element Blocked* and *Get WebElement At* and you have quite powerful way to prevent test failures that you are not really intersted at.

* Is Element Blocked **Locator**

  * Convenience function to check if element is blocked by some other element. Returns boolean value based on the state.

* Element Should Be Blocked / Element Should Not Be Blocked **Locator**

  * Asserts for checking if element is/is not blocked by anything.

* Get Log  **LogType**

  * If underlaying webdriver supports it, returns given logtype logs.

* Get Default Capabilities **BrowserName**

  * Returns a dict of default capabilties. Useful if you need to construct desired_capabilities and you dont need to remember all basic things you need to have. This is due to SeleniumLibrary not providing those defaults anymore if user provide their own.

* Set Element Attribute   **locator**  **attribute_name** **value**

  * Sets arbituary attribute of the element into provided value

* Get Log   **log_type**

  * Returns log_type logs from current browser. If Browser is firefox and profile generated with Generate Firefox Profile keyword is used, Get Log is also able to return browser type logs for it.

* Generate Firefox Profile **options** **accept_untrusted_certs** **proxy**

  * Generates firefox with given options. Also can disable ssl cert checking and setting the proxy.

# Keyword Documentation

Keyword documentation [here](https://salabs.github.io/robotframework-seleniumtestability/index.html) and if you need to create one for offline usage:

```
python -m robot.libdoc SeleniumLibrary::plugins=SeleniumTestability
```



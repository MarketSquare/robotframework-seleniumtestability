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


# Keyword Documentation

At the moment, no online keyword documentation is avaialble but you can create one after
installation:

```
python -m robot.libdoc SeleniumLibrary::plugins=SeleniumTestability
```

This is mainly due to SeleniumLibrary being *plugin* of SeleniumLibrary and it is intended
to be used with it

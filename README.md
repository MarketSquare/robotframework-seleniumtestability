robotframework-seleniumtestability
==================================

SeleniumTestability is a plugin to Robot Framework's SeleniumLibrary that adds
functionality to it doesn't fit into its mission. These new features are archived
by SL's plugin api that then automatically instrumentents the web application via
javascript calls and provides  keywords to bridge those into Robot Framework.

Plugin provides automatic detection of asyncronous events happening within
the web application. For example, if a rest api is called from the application,
testcase can automatically wait for that call to finish before doing any
interaction in the UI. There's also a bunch of functionality like fetching of
browser logs,  keywords to interact with local and session storage.  See the
keyword documentation [here](https://marketsquare.github.io/robotframework-seleniumtestability/index.html?tag=plugin)
for more details.

SeleniumTestability relies on core Selenium's feature EventFiringWebdriver
and provides it's own listener interface that takes care of waiting in right
places and instrumenting the SUT whenever it is needed.

In the future, its also possible to extend the javascript parts of
SeleniumTestability to incorporate more state inspections.

Monitoring of the asyncronous events is archived with help of [Testability.js](https://github.com/alfonso-presa/testability.js)
and its [bindings](https://github.com/alfonso-presa/testability-browser-bindings)

# Support

"Official" support channel available in [Gitter.im](https://gitter.im/robotframework-seleniumtestability/community)

# Installation

```
pip install robotframework-seleniumtestability
```

# Usage

## Initialize library

```
Library         SeleniumLibrary     plugins=SeleniumTestability;True;30 Seconds;True
```

For parameter descriptions, refer to keyword docmentation.

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

* setTimeout & setImmediate calls and wait for them.
* fetch() call and wait for it to finish
* XHR requests and wait for them to finish
* CSS Animations and wait form them to finish
* CSS Transitions and wait form them to finish
* Viewport scrolling.

Do note that catching css animations and transitions is browser dependant. In the past
certain browsers did not implement these features as "the standard" would require.

# Other functionality.

SeleniumTestability also provides other conveniance keywords that do not make sense to incorporate into
SeleniumLibrary itself, mainly due to functionality not being in scope of SeleniumLibrary and Selenium
python bindings. Do check the keyword documentation for up to date list of keywords.


# Keyword Documentation

Keyword documentation [here](https://marketsquare.github.io/robotframework-seleniumtestability/index.html?tag=plugin) and if you need to create one for offline usage:

```
python -m robot.libdoc SeleniumLibrary::plugins=SeleniumTestability
```

# Contributing

[CONTRIBUTING.md](https://github.com/marketsquare/robotframework-seleniumtestability/blob/master/CONTRIBUTING.md) documents how to setup the environment for further development of SeleniumTestability.


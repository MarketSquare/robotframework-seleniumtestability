robotframework-seleniumtestability
==================================

Extension library for SeleniumLibrary that provides either manual or automatic
waiting asyncronous events within SUT.

This is accomplished by utilizing following 2 libraries. First one provides an
API and second one provides bindings.

 * https://github.com/alfonso-presa/testability.js
 * https://github.com/alfonso-presa/testability-browser-bindings


# Installation

```
pip install robotframework-seleniumtestability
```

# Usage

## Initialize library

```
Library         SeleniumLibrary
Library         SeleniumTestability     enable_implicit_wait=True
```

If `enable_implicit_wait` is set to true, just before a selenium library keyword 
is executed, SeleniumTestability library will wait until testability.js api call
returns.  Example:

```
  Click Element   id:button_that_triggers_ajax_request
  Click Element   id:some_other_element
```

In above example, second `Click Element` keyword wont be executed before action 
triggered by the button is finished.

If the `enable_implicit_wait` is set to false, user needs to call `Wait For
Testability Ready` keyword manually. Example:

```
  Click Element   id:button_that_triggers_ajax_request
  Wait For Testability Ready
  Click Element   id:some_other_element
```

## Instrumenting the SUT

Because functionality provided by SeleniumTestability relies on predefined 
javascript api's to be present in the SUT (eg, your web application) before it 
actually works, SUT itself must be instrumented. There are few options to do 
that:

### `Instrument Browser`-keyword

After your tests have loaded the webpage you are testing, call `Instrument Browser`
keyword to inject all required javascript code into the sut. 

Do note: if page is reloaded or your tests scripts navigate out from the page, you 
need re-instrument the browser again.  This should not be the case with single 
page applications as typically the javascript context remains the same.

### Direct integration.

Inject api.js & bindings.js from testability folder into your application's js 
bundle and call instrumentBrowser() javascript at the startup. This procedure 
varies a lot from due to various tooling. Talk to your developers about the 
possibility. 

This could also be archived by MITM Proxy.

Benefit of integration testability api into the application directly is about
timing. If the application initialization triggers any asyncronous actions, 
these are already being detected and there's no need for waiting in the begining 
for a good state when your testing script can start.


# Current Features

* Can detect setTimeout & setImmediate calls and wait for them.
* Can detect fetch() call and wait for it to finish
* Can detect XHR requests and wait for them to finish
* Can detect CSS Animations and wait form them to finish
* Can detect CSS Transitions and wait form them to finish

Do note that CSS animations and transitions do not work properly in Chrome.


# Documentation

  * Keyword Documentation http://omenia.github.io/robotframework-seleniumtestability

# TODO:

* Support ES6 Promises
* Support fetching browser logs from Firefox.
* Investigate on possibility of polyfilling css animations and transitions in
  Chrome.
* Addon possibility for bindings. For example, one might want to extend the
  functionality to support asyncronous actions of any web framework (like
  Angular, React and what not)
* Implement other Keywords that might be useful for testing purposes:
  * Remove Element From DOM

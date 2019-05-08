from SeleniumLibrary.locators import ElementFinder
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError
from robot.utils import timestr_to_secs, secs_to_timestr, type_name
from robot.errors import ExecutionFailed
from robot.api import logger    # noqa: F401
from os.path import dirname, abspath
from .version import VERSION

js_wait_for_testability = """
    var readyCallback = arguments[arguments.length - 1];
    window.testability.when.ready(function() {
        readyCallback(true)
    });
"""

js_wait_for_document_ready = """
    var readyCallback = arguments[arguments.length - 1];
    var checkReadyState=function() {
        document.readyState !== 'complete' ?  setTimeout(checkReadyState, 50) : readyCallback(true);
    };
    checkReadyState();
"""

js_instrument_browser = """
    window.instrumentBrowser(window)
"""

js_is_installed = """
    return window.testability !== undefined && window.instrumentBrowser !== undefined
"""


def explicit_wait_for_testability_ready(error_on_timeout, timeout, selib):
    try:
        WebDriverWait(selib._current_browser(), timeout, 0.15).until(lambda x: selib._current_browser().execute_async_script(js_wait_for_testability))
    except TimeoutException:
        if error_on_timeout:
            raise TimeoutException('Timed out waiting for testability ready callback to trigger.')
    except Exception as e:
        logger.warn(e)


class testabilityElementFinder(ElementFinder):
    def __init__(self, timeout=30.0, error_on_timeout=False, enable_implicit_wait=True):
        super(testabilityElementFinder, self).__init__(self._selib)
        self.timeout = timeout
        self.error_on_timeout = error_on_timeout
        self.enable_implicit_wait = enable_implicit_wait
        self.browser_warning_shown = False
        self.noncompiliant_browsers = ['chrome']

    def is_noncompiliant_browser(self):
        try:
            browser = self._selib._current_browser()
            if 'browserName' in browser.capabilities:
                browserName = browser.capabilities['browserName']
                return browserName in self.noncompiliant_browsers
        except Exception as e:
            logger.debug(e)
            return True

    def find(self, locator, tag=None, first_only=True, required=True, parent=None):
        if self.enable_implicit_wait:
            if not self.browser_warning_shown and self.is_noncompiliant_browser():
                self.browser_warning_shown = True

            explicit_wait_for_testability_ready(self.error_on_timeout, self.timeout, self._selib)

        elements = ElementFinder.find(self, locator, tag, first_only, required, parent)
        return elements

    @property
    def _selib(self):
        return BuiltIn().get_library_instance('SeleniumLibrary')


class SeleniumTestability:
    """Extension library for SeleniumLibrary that provides either manual or automatic waiting asyncronous events within SUT.  This is accomplished by utilizing following 2 libraries.  [ https://github.com/alfonso-presa/testability.js |First one] provides an API and [ https://github.com/alfonso-presa/testability-browser-bindings | second one ] provides bindings.

    When the SUT has been instrumented for testability, library provides a keyword that user can call in the testcode that prevents execution of seleniun keyword until the state of the SUT allows it.  Alternatively, if implicit wait is enabled - either by initializing the library enable_implicit_wait set to True or called `Enable Implicit Wait For Testability`keyword, this waiting will happen automatically so that there is no extra keyword calls required from tests.

    == Usage ==

    == Instrumentation ==
    Your webpage needs to load 2 javascript files and then instrument the running application. Loading can happen by either including api and bindings javascript files into your js bundle and then calling "window.instrumentBrowser()" or by injecting those from the tests directly. First one is preferred as it quarantees that asyncronous events triggered at the startup are also caught.

    Example:
    | ***** Settings *****
    | Library   SeleniumLibrary
    | Library   SeleniumTestability     enable_implicit_wait=True
    |
    | Suite Setup       Open Browser    https://127.0.0.1:5000/   browser=Firefox
    | Suite Teardown    Close Browser
    |
    | ***** Test Cases *****
    | Instrument Browser Example
    |   `Instrument Browser`
    |   ${x}=   `Is Testability Installed`
    |   Should Be True    ${x}

    Here we are instrumenting the browser with `Instrument Browser` keyword and then checking if that was succesful with `Is Testability Installed`.

    ==  Waiting ==
    There are two modes of waiting, implicit and explicit. When Implicit waiting is enabled, when ever you use SeleniumLibrary keywords that uses a locator, this library waits until all currently running and supported asyncronous events are done before commencing to use the locator.
    === Implicit ===
    | ***** Settings *****
    | Library   SeleniumLibrary
    | Library   SeleniumTestability     enable_implicit_wait=True
    |
    | Suite Setup       Open Browser    https://127.0.0.1:5000/   browser=Firefox
    | Suite Teardown    Close Browser
    |
    | ***** Test Cases *****
    | Basic Example
    |   `Instrument Browser`
    |   Click Element     id:fetch-button
    |   Click Element     id:xhr-button
    |   `Wait For Testability Ready`

    In this scenario, test is clicking first element, waits for the fetch call to finish before clicking on the next. Also, do note that in this example, we are calling `Wait For Testability Ready` to also wait for xhr request to finish as there is no other SeleniumLibrary calls after the second click.

    === Explicit ===
    | ***** Settings *****
    | Library   SeleniumLibrary
    | Library   SeleniumTestability     enable_implicit_wait=False
    |
    | Suite Setup       Open Browser    https://127.0.0.1:5000/   browser=Firefox
    | Suite Teardown    Close Browser
    |
    | ***** Test Cases *****
    | Basic Example
    |   `Instrument Browser`
    |   Click Element     id:fetch-button
    |   `Wait For Testability Ready`
    |   Click Element     id:xhr-button
    |   `Wait For Testability Ready`


    = Current Features =
    - Can detect setTimeout & setImmediate calls and wait for them.
    - Can detect fetch() call and wait for it to finish
    - Can detect XHR requests and wait for them to finish
    - Can detect CSS Animations and wait form them to finish
    - Can detect CSS Transitions and wait form them to finish

    *Do note* that CSS animations and transitions do not work properly in *Chrome* as it's not implementing required features yet.

    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self,
                 timeout=30.0,
                 error_on_timeout=False,
                 enable_implicit_wait=True):
        """
        Parameters:
        - ``timeout`` Amount of time to wait until giving up for testability to be ready
        - ``error_on_timeout`` if timeout occurs, should we throw an error
        - ``enable_implicit_wait`` should implicit waiting occur by default. Can be toggled later on with `Enable Implicing Waiting For Testability` and `Disable Implicit Waiting For Testability` keywords.

        """

        self.timeout = timeout
        self.element_finder_installed = False
        self.error_on_timeout = error_on_timeout
        self.enable_implicit_wait = enable_implicit_wait
        self.base_path = dirname(abspath(__file__))
        if self.enable_implicit_wait:
            self.element_finder_installed = self._install_element_finder(self.timeout, self.error_on_timeout, self.enable_implicit_wait)

    def _install_element_finder(self, timeout, error_on_timeout, enable_implicit_wait):
        if not self.element_finder_installed:
            result = False
            try:
                self._old_element_finder = self._selib._element_finder
                self._selib._element_finder = testabilityElementFinder(timeout, error_on_timeout, enable_implicit_wait)
                result = True
            except RobotNotRunningError:
                pass
        return result

    def _toggle_implicit_wait_for_testability(self, state=True):
        if not isinstance(state, bool):
            raise TypeError("state must be boolean, got %s instead." % type_name(state))

        if not self.element_finder_installed and state:
            self.element_finder_installed = self._install_element_finder(self.timeout, self.error_on_timeout, self.enable_implicit_wait)

        if not self.element_finder_installed:
            if state:
                raise ExecutionFailed("testabilityElementFinder is not currently installed")
            else:
                return

        self._selib._element_finder.enable_implicit_wait = state

    def enable_implicit_wait_for_testability(self):
        """
        Enables implicit waiting
        """
        self._toggle_implicit_wait_for_testability(True)

    def disable_implicit_wait_for_testability(self):
        """
        Disables implicit waiting
        """
        self._toggle_implicit_wait_for_testability(False)

    def get_implicit_wait_timeout(self):
        """
        Returns the currently set value of timeout.
        """
        if not self.element_finder_installed:
            raise ExecutionFailed("testabilityElementFinder is not currently installed")

        return secs_to_timestr(self.timeout)

    def set_implicit_wait_timeout(self, seconds):
        """
        Sets the value to timeout.
        Parameters:
        - ``seconds`` - in seconds

        """
        if not self.element_finder_installed:
            raise ExecutionFailed("testabilityElementFinder is not currently installed")

        old_timeout = self.get_implicit_wait_timeout()
        self.timeout = timestr_to_secs(seconds)
        self._selib._element_finder.timeout = self.timeout
        return old_timeout

    def wait_for_testability_ready(self, timeout=None, error_on_timeout=False):
        """
        Explicitly waits until testability is ready or timeout happens.
        Parameters:
        - ``timeout`` Amount of time to wait until giving up for testability to be ready
        - ``error_on_timeout`` if timeout occurs, should we throw an error
        """

        if timeout:
            timeoutSecs = timestr_to_secs(timeout)
        else:
            timeoutSecs = self.timeout

        explicit_wait_for_testability_ready(self.error_on_timeout, timeoutSecs, self._selib)

    def wait_for_document_ready(self):
        """
        Explicit waits until document.readyState is complete.
        """
        self._selib.execute_async_javascript(js_wait_for_document_ready)

    def _inject_testability(self):
        with open("{}/testability/api_inject.js".format(self.base_path), 'r') as f:
            buf = f.read()
            self._selib.execute_javascript("{}; window.testability = testability;".format(buf))

        with open("{}/testability/bindings.js".format(self.base_path), 'r') as f:
            buf = f.read()
            self._selib.execute_javascript("{}; window.instrumentBrowser = instrumentBrowser;".format(buf))

    def instrument_browser(self):
        """
        Instruments the current webpage for testability. If dependant javascript files are not part of the webpage, they are injected. And then, javascript call instrumentBrowser() is called in order catch all asyncronous and supported events.
        """
        if not self.is_testability_installed():
            self._inject_testability()

        self._selib.execute_javascript(js_instrument_browser)

    def is_testability_installed(self):
        """
        Returns True if testability api's are loaded, False if not.
        """
        return self._selib.execute_javascript(js_is_installed)

    @property
    def _selib(self):
        return BuiltIn().get_library_instance('SeleniumLibrary')

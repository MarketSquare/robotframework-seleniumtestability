from SeleniumLibrary.locators import ElementFinder
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from robot.libraries.BuiltIn import BuiltIn
from robot.utils import timestr_to_secs, secs_to_timestr, type_name
from robot.api import logger    # noqa: F401
from os.path import dirname, abspath
from .version import get_version

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
        self.offending_browsers = ['chrome']

    def _not_so_good_browser(self):
        try:
            browser = self._selib._current_browser()
            if 'browserName' in browser.capabilities:
                browserName = browser.capabilities['browserName']
                return browserName in self.offending_browsers
        except Exception as e:
            logger.debug(e)
            return True

    def find(self, locator, tag=None, first_only=True, required=True, parent=None):
        if self.enable_implicit_wait:
            if not self.browser_warning_shown and self._not_so_good_browser():
                self.browser_warning_shown = True
                logger.warn("All currently supported testability features are not implemented in your browser")

            explicit_wait_for_testability_ready(self.error_on_timeout, self.timeout, self._selib)

        elements = ElementFinder.find(self, locator, tag, first_only, required, parent)
        return elements

    @property
    def _selib(self):
        return BuiltIn().get_library_instance('SeleniumLibrary')


class SeleniumTestability:

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = get_version()

    def __init__(self,
                 timeout=30.0,
                 error_on_timeout=False,
                 enable_implicit_wait=True):
        """
        = SeleniumTestability Library =
        SeleniumTestability is extension library for SeleniumLibrary that provides
        either manual or automatic waiting asyncronous events within SUT.

        This is accomplished by utilizing following 2 libraries. First one provides
        API and second one provides bindings.

        - https://github.com/alfonso-presa/testability.js
        - https://github.com/alfonso-presa/testability-browser-bindings

        When the SUT has been instrumented for testability, library provides a
        keyword that user can call in the testcode that prevents execution of
        seleniun keyword until the state of the SUT allows it. Alternatively,
        depending on how the the library has initialized, this waiting can happen
        automatically so that there is no extra code required from test code
        itself.

        == Usage ==

        == Instrumentation ==
        TODO
        ==  Waiting ==
        === Explicit ===
        TODO
        === Implicit Waiting ===
        TODO

        """

        self.timeout = timeout
        self.error_on_timeout = error_on_timeout
        self.enable_implicit_wait = enable_implicit_wait
        self.base_path = dirname(abspath(__file__))

        self._selib._element_finder = testabilityElementFinder(timeout, error_on_timeout, enable_implicit_wait)

    def enable_implicit_wait_for_testability(self, state=True):
        """
        TODO: Wait For Testability Ready keyword
        """
        if not isinstance(state, bool):
            raise TypeError("state must be boolean, got %s instead." % type_name(state))

        self._selib._element_finder.enable_implicit_wait = state

    def disable_implicit_wait_for_testability(self):
        """
        TODO: Wait For Testability Ready keyword
        """
        self.enable_implicit_wait_for_testability(False)

    def get_implicit_wait_timeout(self):
        """
        TODO: Wait For Testability Ready keyword
        """
        return secs_to_timestr(self.timeout)

    def set_implicit_wait_timeout(self, seconds):
        """
        TODO: Wait For Testability Ready keyword
        """
        old_timeout = self.get_implicit_wait_timeout()
        self.timeout = timestr_to_secs(seconds)
        self._selib._element_finder.timeout = self.timeout
        return old_timeout

    def wait_for_testability_ready(self, timeout=None, message=None):
        """
        TODO: Wait For Testability Ready keyword
        """

        if timeout:
            timeoutSecs = timestr_to_secs(timeout)
        else:
            timeoutSecs = self.timeout

        explicit_wait_for_testability_ready(self.error_on_timeout, timeoutSecs, self._selib)

    def wait_for_document_ready(self):
        """
        TODO: Wait For Document Ready keyword
        """
        self._selib.execute_async_javascript(js_wait_for_document_ready)

    def _inject_testability(self):
        """
        TODO: Inject Testability docs
        """
        with open("{}/testability/api_inject.js".format(self.base_path), 'r') as f:
            buf = f.read()
            self._selib.execute_javascript("{}; window.testability = testability;".format(buf))

        with open("{}/testability/bindings.js".format(self.base_path), 'r') as f:
            buf = f.read()
            self._selib.execute_javascript("{}; window.instrumentBrowser = instrumentBrowser;".format(buf))

    def instrument_browser(self):
        """
        TODO: Instrument Browser docs
        """
        if not self.is_testability_installed():
            self._inject_testability()

        self._selib.execute_javascript(js_instrument_browser)

    def is_testability_installed(self):
        """
        TODO: Is Testability Installed
        """
        return self._selib.execute_javascript(js_is_installed)

    @property
    def _selib(self):
        return BuiltIn().get_library_instance('SeleniumLibrary')

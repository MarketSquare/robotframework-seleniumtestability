from SeleniumLibrary.base import LibraryComponent, keyword
from SeleniumLibrary.keywords.javascript import JavaScriptKeywords
from os.path import abspath, dirname
from .listener import TestabilityListener
from .javascript import JS_LOOKUP
from robot.utils import is_truthy, timestr_to_secs, secs_to_timestr
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from furl import furl


class SeleniumTestability(LibraryComponent):
    """
    SeleniumTestability is plugin for SeleniumLibrary that provides either manual or automatic waiting asyncronous events within SUT. This works by injecting small javascript snippets that can monitor the web application's state and when any supported events are happening within the sut, execution of SeleniumLibrary's keywords are blocked until timeout or those events are processed.

    On top of this, there are some more or less useful utilities for web application testing.

    TODO: Document constructor variables and Listener

    == Usage ==

    Example:
    | ***** Settings *****
    | Library   SeleniumLibrary    plugins=SeleniumTestability;True;30 Seconds;True
    |
    | Suite Setup       Open Browser    https://127.0.0.1:5000/   browser=Firefox
    | Suite Teardown    Close Browser
    |
    | ***** Test Cases *****
    | Instrument Browser Example
    |   ${x}=   `Testability Loaded`
    |   Should Be True    ${x}


    ==  Waiting ==

    There are two modes of waiting, automatic and non-automatic. When automatic waiting is enabled, when SeleniumLibrary keywords are used, plugin waits until all currently running and supported asyncronous events are done before commencing to use the locator.

    === Automatic ===
    | ***** Settings *****
    | Library   SeleniumLibrary    plugins=SeleniumTestability;True;30 Seconds;True
    |
    | Suite Setup       Open Browser    https://127.0.0.1:5000/   browser=Firefox
    | Suite Teardown    Close Browser
    |
    | ***** Test Cases *****
    | Basic Example
    |   Click Element     id:fetch-button
    |   Click Element     id:xhr-button
    |   `Wait For Testability Ready`
    In this scenario, test is clicking first element, waits for the fetch call to finish before clicking on the next. Also, do note that in this example, we are calling `Wait For Testability Ready` to also wait for xhr request to finish as there is no other SeleniumLibrary calls after the second click.

    === Non Automatic ===
    | ***** Settings *****
    | Library   SeleniumLibrary    plugins=SeleniumTestability;False;30 Seconds;True
    |
    | Suite Setup       Open Browser    https://127.0.0.1:5000/   browser=Firefox
    | Suite Teardown    Close Browser
    |
    | ***** Test Cases *****
    | Basic Example
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

    *Do note* that CSS animations and transitions might not work properly in *Chrome*.

    """

    @property
    def automatic_wait(self):
        return self.ctx.testability_settings["automatic_wait"]

    @automatic_wait.setter
    def automatic_wait(self, value):
        self.ctx.testability_settings["automatic_wait"] = is_truthy(value)

    @property
    def error_on_timeout(self):
        return self.ctx.testability_settings["error_on_timeout"]

    @error_on_timeout.setter
    def error_on_timeout(self, value):
        self.ctx.testability_settings["error_on_timeout"] = is_truthy(value)

    @property
    def timeout(self):
        return self.ctx.testability_settings["timeout"]

    @timeout.setter
    def timeout(self, value):
        self.ctx.testability_settings["timeout"] = timestr_to_secs(value)

    @property
    def automatic_injection(self):
        return self.ctx.testability_settings["automatic_injection"]

    @automatic_injection.setter
    def automatic_injection(self, value):
        self.ctx.testability_settings["automatic_injection"] = is_truthy(value)

    def __init__(self, ctx, automatic_wait=True, timeout="30 seconds", error_on_timeout=True, automatic_injection=True):
        LibraryComponent.__init__(self, ctx)
        try:
            self.ctx.__doc__ = "{}\n\n= SeleniumTestability =\n{}".format(self.ctx.__doc__, self.__doc__)
        except AttributeError:
            # plugin will get initialized on every import and at some point __doc__ becomes read-only
            pass
        self.debug("SeleniumTestability: __init_({},{},{},{},{})".format(ctx, automatic_wait, timeout, error_on_timeout, automatic_injection))  # This does not work
        self.js = JavaScriptKeywords(ctx)
        self.CWD = abspath(dirname(__file__))
        self.api_file = "{}/js/api_inject.js".format(self.CWD)
        self.bindings_file = "{}/js/bindings.js".format(self.CWD)
        self.ctx.event_firing_webdriver = TestabilityListener
        self.ctx.testability_settings = {"testability": self}
        self.automatic_wait = automatic_wait
        self.automatic_injection = automatic_injection
        self.error_on_timeout = error_on_timeout
        self.timeout = timeout

    @keyword
    def inject_testability(self):
        """
        Injects SeleniumTestability javascript bindings into a current browser's current window. This should happen automatically vie SeleniumTestability's internal `Event Firing Webdriver` support but keyword is provided also.
        """
        self.debug("SeleniumTestability: inject_testability()")
        with open(self.api_file, 'r') as f:
            buf = f.read()
            self.js.execute_javascript("{}; window.testability = testability;".format(buf))

        with open(self.bindings_file, 'r') as f:
            buf = f.read()
            self.js.execute_javascript("{}; window.instrumentBrowser = instrumentBrowser;".format(buf))

    @keyword
    def instrument_browser(self):
        """
        Instruments the current webpage for testability. This should happen automatically vie SeleniumTestability's internal `Event Firing Webdriver` support but keyword is provided also. Calls `Inject Testability` keyword automatically.
        """
        self.debug("SeleniumTestability: instrument_browser()")
        if not self.is_testability_installed():
            self.inject_testability()
            self.js.execute_javascript(JS_LOOKUP["instrument_browser"])

    @keyword
    def is_testability_installed(self):
        """
        Returns True if testability api's are loaded and current browser/window is instrumented, False if not.
        """
        self.debug("SeleniumTestability:  is_testability_installed()")
        return self.js.execute_javascript(JS_LOOKUP["is_installed"])

    @keyword
    def wait_for_document_ready(self):
        """
        Explicit waits until document.readyState is complete.
        """
        self.debug("SeleniumTestability:  wait_for_document_ready()")
        self.js.execute_async_javascript(JS_LOOKUP["wait_for_document_ready"])

    @keyword
    def set_testability_automatic_wait(self, enabled):
        """
        Sets the state to TestabilityListener if it should automically call `Wait For Testability Ready` when interactions are done.
        Parameters:
         - ``enabled`` state of automatic waits.
        """
        self.debug("SeleniumTestability: set_testability_automatic_wait({})".format(enabled))
        self.automatic_wait = enabled

    @keyword
    def enable_testability_automatic_wait(self):
        """
        Enables TestabilityListener to call `Wait For Testability Ready` onn all interactions that are done.
        """
        self.debug("SeleniumTestability:  enable_testability_automatic_wait()")
        self.set_testability_automatic_wait(True)

    @keyword
    def disable_testability_automatic_wait(self):
        """
        Disables TestabilityListener to call `Wait For Testability Ready` onn all interactions that are done.
        """
        self.debug("SeleniumTestability:  disable_testability_automatic_wait()")
        self.set_testability_automatic_wait(False)

    @keyword
    def wait_for_testability_ready(self, timeout=None, error_on_timeout=None):
        """
        Explicitly waits until testability is ready or timeout happens.
        Parameters:
        - ``timeout`` Amount of time to wait until giving up for testability to be ready. Robot framework timestring
        - ``error_on_timeout`` if timeout occurs, should we throw an error

        Both parameters are optional, if not provided, default values from plugin initialization time are used.
        """
        local_timeout = self.timeout
        if timeout is not None:
            local_timeout = timestr_to_secs(timeout)
        local_error_on_timeout = self.error_on_timeout
        if error_on_timeout is not None:
            local_error_on_timeout = is_truthy(error_on_timeout)

        try:
            WebDriverWait(self.ctx.driver, local_timeout, 0.15).until(lambda x: self.js.execute_async_javascript(JS_LOOKUP["wait_for_testability"]))
        except TimeoutException:
            if local_error_on_timeout:
                raise TimeoutException('Timed out waiting for testability ready callback to trigger.')
        except Exception as e:
            self.warn(e)

    @keyword
    def set_testability_timeout(self, timeout):
        """
        Sets the global timeout value for waiting testability ready. Overrides the defaults set from plugin parameters.
        Parameters:
        - ``timeout`` Amount of time to wait until giving up for testability to be ready. Robot framework timestring
        """
        current = self.timeout
        self.timeout = timeout
        return secs_to_timestr(current)

    @keyword
    def get_testability_timeout(self):
        """
        Returns the global timeout value in robot framework timestr format for waiting testability ready.
        """
        return secs_to_timestr(self.timeout)

    @keyword
    def set_testability_error_on_timeout(self, error_on_timeout):
        """Sets the global error_on_timeout value. eg, should SeleniumTestability throw exception when timeout occurs and there are still events in the testability queue.
        Parameters:
        - ``error_on_timeout``  - any value that robot framework considers truthy can be provided here.
        """
        self.error_on_timeout = error_on_timeout

    @keyword
    def get_testability_error_on_timeout(self):
        """Returns error_on_timeout value set via plugin parameters or via `Set Testability Error On Timeout`keyword.
        """
        return self.error_on_timeout

    @staticmethod
    @keyword("Add Basic Authentication To Url")
    def add_authentication(url, user, password):
        """
        For websites that require basic auth authentication, add user and password into the given url.
        Parameters:
        - ``url``  - url where user and password should be added to.
        - ``user``  - username
        - ``password``  - password
        """
        data = furl(url)
        data.username = user
        data.password = password
        return data.tostr()

    @staticmethod
    @keyword
    def split_url_to_host_and_path(url):
        """
        Returs given url as dict with property "base" set to a protocol and hostname and "path" as the trailing path.
        This is useful when constructing requests sessions from urls used within SeleniumLibrary.
        """
        data = furl(url)
        return {'base': str(data.copy().remove(path=True)), 'path': str(data.path)}

    @keyword
    def set_testability_automatic_injection(self, enabled):
        """
        Sets the state to TestabilityListener if it should automically inject testability.
        Parameters:
         - ``enabled`` state of automatic injection
        """
        self.debug("SeleniumTestability: set_testability_automatic_injection({})".format(enabled))
        self.automatic_injection = enabled

    @keyword
    def enable_testability_automatic_injection(self):
        """
        Enables TestabilityListener to automatically inject testability.
        """
        self.debug("SeleniumTestability:  enable_testability_automatic_injection()")
        self.set_testability_automatic_injection(True)

    @keyword
    def disable_testability_automatic_injection(self):
        """
        Disables TestabilityListener to automatically inject testability
        """
        self.debug("SeleniumTestability:  disable_testability_automatic_injection()")
        self.set_testability_automatic_injection(False)

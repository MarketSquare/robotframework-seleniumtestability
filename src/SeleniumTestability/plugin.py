# -*- coding: utf-8 -*-
from SeleniumLibrary.base import LibraryComponent, keyword
from SeleniumLibrary.keywords.element import ElementKeywords
from SeleniumLibrary import SeleniumLibrary
from os.path import abspath, dirname
from .listener import TestabilityListener
from .javascript import JS_LOOKUP
from .types import WebElementType, LocatorType, OptionalBoolType, OptionalStrType, BrowserLogsType, OptionalDictType
from robot.utils import is_truthy, timestr_to_secs, secs_to_timestr
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, WebDriverException
from http.cookies import SimpleCookie
from furl import furl
from typing import Dict
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


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

    BROWSERS = {
        "googlechrome": DesiredCapabilities.CHROME,
        "gc": DesiredCapabilities.CHROME,
        "chrome": DesiredCapabilities.CHROME,
        "headlesschrome": DesiredCapabilities.CHROME,
        "ff": DesiredCapabilities.FIREFOX,
        "firefox": DesiredCapabilities.FIREFOX,
        "headlessfirefox": DesiredCapabilities.FIREFOX,
        "ie": DesiredCapabilities.INTERNETEXPLORER,
        "internetexplorer": DesiredCapabilities.INTERNETEXPLORER,
        "edge": DesiredCapabilities.EDGE,
        "opera": DesiredCapabilities.OPERA,
        "safari": DesiredCapabilities.SAFARI,
        "phantomjs": DesiredCapabilities.PHANTOMJS,
        "htmlunit": DesiredCapabilities.HTMLUNIT,
        "htmlunitwithjs": DesiredCapabilities.HTMLUNITWITHJS,
        "android": DesiredCapabilities.ANDROID,
        "iphone": DesiredCapabilities.IPHONE,
    }

    @property
    def automatic_wait(self: "SeleniumTestability") -> bool:
        return self.ctx.testability_settings["automatic_wait"]

    @automatic_wait.setter
    def automatic_wait(self: "SeleniumTestability", value: bool) -> None:
        self.ctx.testability_settings["automatic_wait"] = value

    @property
    def error_on_timeout(self: "SeleniumTestability") -> bool:
        return self.ctx.testability_settings["error_on_timeout"]

    @error_on_timeout.setter
    def error_on_timeout(self: "SeleniumTestability", value: bool) -> None:
        self.ctx.testability_settings["error_on_timeout"] = value

    @property
    def timeout(self: "SeleniumTestability") -> float:
        return self.ctx.testability_settings["timeout"]

    @timeout.setter
    def timeout(self: "SeleniumTestability", value: str) -> None:
        self.ctx.testability_settings["timeout"] = timestr_to_secs(value)

    @property
    def automatic_injection(self: "SeleniumTestability") -> bool:
        return self.ctx.testability_settings["automatic_injection"]

    @automatic_injection.setter
    def automatic_injection(self: "SeleniumTestability", value: bool) -> None:
        self.ctx.testability_settings["automatic_injection"] = value

    def __init__(
        self: "SeleniumTestability",
        ctx: SeleniumLibrary,
        automatic_wait: bool = True,
        timeout: str = "30 seconds",
        error_on_timeout: bool = True,
        automatic_injection: bool = True,
    ) -> None:
        LibraryComponent.__init__(self, ctx)
        try:
            self.ctx.__doc__ = "{}\n\n= SeleniumTestability =\n{}".format(self.ctx.__doc__, self.__doc__)
        except AttributeError:
            # plugin will get initialized on every import and at some point __doc__ becomes read-only
            pass
        self.debug(
            "SeleniumTestability: __init_({},{},{},{},{})".format(
                ctx, automatic_wait, timeout, error_on_timeout, automatic_injection
            )
        )  # This does not work
        self.el = ElementKeywords(ctx)
        self.CWD = abspath(dirname(__file__))
        self.js_bundle = "{}/js/testability.js".format(self.CWD)
        self.ctx.event_firing_webdriver = TestabilityListener
        self.ctx.testability_settings = {"testability": self}
        self.automatic_wait = automatic_wait
        self.automatic_injection = automatic_injection
        self.error_on_timeout = error_on_timeout
        self.timeout = timeout  # type: ignore
        self.hidden_elements = {}  # type: Dict[str, str]
        self.browser_warn_shown = False
        self.empty_log_warn_shown = False

    def _inject_testability(self: "SeleniumTestability") -> None:
        """
        Injects SeleniumTestability javascript bindings into a current browser's current window. This should happen automatically vie SeleniumTestability's internal `Event Firing Webdriver` support but keyword is provided also.
        """
        self.debug("SeleniumTestability: _inject_testability()")
        with open(self.js_bundle, "r") as f:
            buf = f.read()
            self.ctx.driver.execute_script("{};".format(buf))

    @keyword
    def instrument_browser(self: "SeleniumTestability") -> None:
        """
        Instruments the current webpage for testability. This should happen automatically vie SeleniumTestability's internal `Event Firing Webdriver` support but keyword is provided also. Calls `Inject Testability` keyword automatically.
        """
        self.debug("SeleniumTestability: instrument_browser()")
        if not self.is_testability_installed():
            self._inject_testability()

    @keyword
    def is_testability_installed(self: "SeleniumTestability") -> bool:
        """
        Returns True if testability api's are loaded and current browser/window is instrumented, False if not.
        """
        self.debug("SeleniumTestability:  is_testability_installed()")
        return self.ctx.driver.execute_script(JS_LOOKUP["is_installed"])

    @keyword
    def wait_for_document_ready(self: "SeleniumTestability") -> None:
        """
        Explicit waits until document.readyState is complete.
        """
        self.debug("SeleniumTestability:  wait_for_document_ready()")
        self.ctx.driver.execute_async_script(JS_LOOKUP["wait_for_document_ready"])

    @keyword
    def set_testability_automatic_wait(self: "SeleniumTestability", enabled: bool) -> None:
        """
        Sets the state to TestabilityListener if it should automically call `Wait For Testability Ready` when interactions are done.
        Parameters:
         - ``enabled`` state of automatic waits.
        """
        self.debug("SeleniumTestability: set_testability_automatic_wait({})".format(enabled))
        self.automatic_wait = enabled

    @keyword
    def enable_testability_automatic_wait(self: "SeleniumTestability") -> None:
        """
        Enables TestabilityListener to call `Wait For Testability Ready` onn all interactions that are done.
        """
        self.debug("SeleniumTestability:  enable_testability_automatic_wait()")
        self.set_testability_automatic_wait(True)

    @keyword
    def disable_testability_automatic_wait(self: "SeleniumTestability") -> None:
        """
        Disables TestabilityListener to call `Wait For Testability Ready` onn all interactions that are done.
        """
        self.debug("SeleniumTestability:  disable_testability_automatic_wait()")
        self.set_testability_automatic_wait(False)

    @keyword
    def wait_for_testability_ready(
        self: "SeleniumTestability", timeout: OptionalStrType = None, error_on_timeout: OptionalBoolType = None
    ) -> None:
        """
        Explicitly waits until testability is ready or timeout happens.
        Parameters:
        - ``timeout`` Amount of time to wait until giving up for testability to be ready. Robot framework timestring
        - ``error_on_timeout`` if timeout occurs, should we throw an error

        Both parameters are optional, if not provided, default values from plugin initialization time are used.
        """
        self.debug("SeleniumTestability:  wait_for_testability_ready({},{})".format(timeout, error_on_timeout))
        local_timeout = self.timeout
        if timeout is not None:
            local_timeout = timestr_to_secs(timeout)
        local_error_on_timeout = self.error_on_timeout
        if error_on_timeout is not None:
            local_error_on_timeout = is_truthy(error_on_timeout)

        try:
            WebDriverWait(self.ctx.driver, local_timeout, 0.15).until(
                lambda x: self.ctx.driver.execute_async_script(JS_LOOKUP["wait_for_testability"])
            )
        except TimeoutException:
            if local_error_on_timeout:
                raise TimeoutException("Timed out waiting for testability ready callback to trigger.")
        except Exception as e:
            self.warn(e)

    @keyword
    def set_testability_timeout(self: "SeleniumTestability", timeout: str) -> str:
        """
        Sets the global timeout value for waiting testability ready. Overrides the defaults set from plugin parameters.
        Parameters:
        - ``timeout`` Amount of time to wait until giving up for testability to be ready. Robot framework timestring
        """
        current = self.timeout
        self.timeout = timeout  # type: ignore
        return secs_to_timestr(current)

    @keyword
    def get_testability_timeout(self: "SeleniumTestability") -> str:
        """
        Returns the global timeout value in robot framework timestr format for waiting testability ready.
        """
        return secs_to_timestr(self.timeout)

    @keyword
    def set_testability_error_on_timeout(self: "SeleniumTestability", error_on_timeout: bool) -> None:
        """Sets the global error_on_timeout value. eg, should SeleniumTestability throw exception when timeout occurs and there are still events in the testability queue.
        Parameters:
        - ``error_on_timeout``  - any value that robot framework considers truthy can be provided here.
        """
        self.error_on_timeout = error_on_timeout

    @keyword
    def get_testability_error_on_timeout(self: "SeleniumTestability") -> bool:
        """Returns error_on_timeout value set via plugin parameters or via `Set Testability Error On Timeout`keyword.
        """
        return self.error_on_timeout

    @staticmethod
    @keyword("Add Basic Authentication To Url")
    def add_authentication(url: str, user: str, password: str) -> str:
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
    def split_url_to_host_and_path(url: str) -> dict:
        """
        Returs given url as dict with property "base" set to a protocol and hostname and "path" as the trailing path.
        This is useful when constructing requests sessions from urls used within SeleniumLibrary.
        """
        data = furl(url)
        return {"base": str(data.copy().remove(path=True)), "path": str(data.path)}

    @keyword
    def set_testability_automatic_injection(self: "SeleniumTestability", enabled: bool) -> None:
        """
        Sets the state to TestabilityListener if it should automically inject testability.
        Parameters:
         - ``enabled`` state of automatic injection
        """
        self.debug("SeleniumTestability: set_testability_automatic_injection({})".format(enabled))
        self.automatic_injection = enabled

    @keyword
    def enable_testability_automatic_injection(self: "SeleniumTestability") -> None:
        """
        Enables TestabilityListener to automatically inject testability.
        """
        self.debug("SeleniumTestability:  enable_testability_automatic_injection()")
        self.set_testability_automatic_injection(True)

    @keyword
    def disable_testability_automatic_injection(self: "SeleniumTestability") -> None:
        """
        Disables TestabilityListener to automatically inject testability
        """
        self.debug("SeleniumTestability:  disable_testability_automatic_injection()")
        self.set_testability_automatic_injection(False)

    @staticmethod
    @keyword
    def cookies_to_dict(cookies: str) -> dict:  # FIX: cookies can be dict also
        """
        Converts a cookie string into python dict.
        """
        ret = {}
        cookie = SimpleCookie()
        cookie.load(cookies)
        for key, morsel in cookie.items():
            ret[key] = morsel.value
        return ret

    @keyword
    def get_current_useragent(self: "SeleniumTestability") -> str:
        """
        Returns useragent string of current browser.
        """
        self.debug("SeleniumTestability:  get_current_useragent()")
        return self.ctx.driver.execute_script(JS_LOOKUP["useragent"])

    @keyword
    def drag_and_drop(self: "SeleniumTestability", locator: LocatorType, target: LocatorType, html5: bool = False) -> None:
        """Drags element identified by ``locator`` into ``target`` element.

        The ``locator`` argument is the locator of the dragged element
        and the ``target`` is the locator of the target. See the
        `Locating elements` section for details about the locator syntax.

        ``html5`` parameter is optional and if provided, `drag_and_drop`will utilize
        javascript to trigger the suitable events ensuring that html5 applications
        receive the right events

        Example:
        | `Drag And Drop` | css:div#element | css:div.target |  True |
        """
        html5 = is_truthy(html5)
        self.debug("SeleniumTestability:  drag_and_drop({},{},{})".format(locator, target, html5))
        if not html5:
            self.el.drag_and_drop(locator, target)
        else:
            from_element = self.el.find_element(locator)
            to_element = self.el.find_element(target)
            self.ctx.driver.execute_script(JS_LOOKUP["dragdrop"], from_element, to_element)

    @keyword
    def scroll_to_bottom(self: "SeleniumTestability") -> None:
        """
        Scrolls current window to the bottom of the page
        """
        self.debug("SeleniumTestability:  scroll_to_bottom()")
        self.ctx.driver.execute_script(JS_LOOKUP["scroll_to_bottom"])

    @keyword
    def scroll_to_top(self: "SeleniumTestability") -> None:
        """
        Scrolls current window to the bottom of the page
        """
        self.debug("SeleniumTestability:  scroll_to_top()")
        self.ctx.driver.execute_script(JS_LOOKUP["scroll_to_top"])

    @keyword
    def toggle_element_visibility(self: "SeleniumTestability", locator: LocatorType) -> None:
        """
        Toggles visiblity state of element via ``locator``
        """
        self.debug("SeleniumTestability:  toggle_element_visibility({})".format(locator))
        if locator in self.hidden_elements:
            self.hide_element(locator)
        else:
            self.show_element(locator)

    @keyword
    def hide_element(self: "SeleniumTestability", locator: LocatorType) -> None:
        """
        Hides element via ``locator``. Typically one would use this to avoid getting
        Toggles visiblity state of element via ``locator``
        past overlays that are on top of element that is to be interacted with.
        """
        self.debug("SeleniumTestability: hide_element({})".format(locator))
        from_element = self.el.find_element(locator)
        current_display = self.ctx.driver.execute_script(JS_LOOKUP["get_style_display"], from_element)
        self.hidden_elements[locator] = current_display
        self.ctx.driver.execute_script(JS_LOOKUP["set_style_display"], from_element, "none")

    @keyword
    def show_element(self: "SeleniumTestability", locator: LocatorType) -> None:
        """
        Shows element via ``locator`` that has been previously been hidden with `Hide Element` keyword.
        """
        self.debug("SeleniumTestability: show_element({})".format(locator))
        from_element = self.el.find_element(locator)
        state = self.hidden_elements.get(locator, "")
        self.ctx.driver.execute_script(JS_LOOKUP["set_style_display"], from_element, state)
        del self.hidden_elements[locator]

    def _element_blocked(self: "SeleniumTestability", locator: LocatorType) -> bool:
        from_element = self.el.find_element(locator)
        rect = self.ctx.driver.execute_script(JS_LOOKUP["get_rect"], from_element)
        y = rect["y"] + (rect["height"] / 2)
        x = rect["x"] + (rect["width"] / 2)
        elem = self.ctx.driver.execute_script(JS_LOOKUP["get_element_at"], x, y)
        try:
            return from_element != elem.wrapped_element
        except AttributeError:
            return from_element != elem

    @keyword
    def get_webelement_at(self: "SeleniumTestability", x: int, y: int) -> WebElementType:
        """Returns a topmost WebElement at given coordinates"""
        element = self.ctx.driver.execute_script(JS_LOOKUP["get_element_at"], x, y)
        # NOTE: Maybe we should always return just straight element  and not
        # really care if its event firing or not?
        try:
            return element.wrapped_element
        except AttributeError:
            return element

    @keyword
    def is_element_blocked(self: "SeleniumTestability", locator: LocatorType) -> bool:
        """
        Returns `True` is ``locator`` is blocked, `False` if it is not.
        Example:
        | ${blocked}=       | Is Element Blocked    | id:some_id    |                  |
        | Run Keyword If    | ${blocked} == True    | Hide  Element | id:some_other_id |
        This will hide the element with id:some_other_id if  element id:some_id is being blocked
        """
        return self._element_blocked(locator)

    @keyword
    def element_should_be_blocked(self: "SeleniumTestability", locator: LocatorType) -> None:
        """
        Throws exception if element found with ``locator`` is not blocked by any overlays.
        #TODO: Add examples
        """
        self.debug("SeleniumTestability: element_should_be_blocked({})".format(locator))
        is_blocked = self._element_blocked(locator)
        self.debug("SeleniumTestability: element_should_be_blocked({}): {}".format(locator, is_blocked))
        if not is_blocked:
            raise AssertionError("Element with locator {} is not blocked".format(locator))

    @keyword
    def element_should_not_be_blocked(self: "SeleniumTestability", locator: LocatorType) -> None:
        """
        Throws exception if element found with ``locator`` is being blocked by overlays.
        #TODO: Add examples
        """
        self.debug("SeleniumTestability: element_should_not_be_blocked({})".format(locator))
        is_blocked = self._element_blocked(locator)
        self.debug("SeleniumTestability: element_should_be_blocked({}): {}".format(locator, is_blocked))
        if is_blocked:
            raise AssertionError("Element with locator {} is blocked".format(locator))

    @keyword
    def get_log(self: "SeleniumTestability", log_type: str = "browser") -> BrowserLogsType:
        """
        Returns logs determined by ``log_type`` from the current browser.
        """
        self.debug("SeleniumTestability: get_log({})".format(log_type))
        ret = []  # type: BrowserLogsType
        try:
            ret = self.ctx.driver.get_log(log_type)
        except WebDriverException:
            if not self.browser_warn_shown:
                self.browser_warn_shown = True
                self.warn("Current browser does not support fetching logs from the browser")
                return []
        if not ret and not self.empty_log_warn_shown:
            self.empty_log_warn_shown = True
            self.warn("No logs available - you might need to enable loggingPrefs in desired_capabilities")
        return ret

    @keyword
    def get_default_capabilities(self: "SeleniumTestability", browser_name: str) -> OptionalDictType:
        """
        Returns a set of default capabilities for given ``browser``.
        """
        try:
            browser = browser_name.lower().replace(" ", "")
            return self.BROWSERS[browser].copy()
        except Exception as e:
            self.debug(e)
            return None

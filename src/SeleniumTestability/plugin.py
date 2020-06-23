# -*- coding: utf-8 -*-
from SeleniumLibrary.base import LibraryComponent, keyword
from SeleniumLibrary.keywords.element import ElementKeywords
from SeleniumLibrary import SeleniumLibrary
from os.path import abspath, dirname, join
from .listener import TestabilityListener
from .javascript import JS_LOOKUP
from .logger import get_logger, argstr, kwargstr
from .types import (
    WebElementType,
    LocatorType,
    OptionalBoolType,
    OptionalStrType,
    BrowserLogsType,
    OptionalDictType,
    is_firefox,
    StringArray,
    StorageType,
)
from robot.utils import is_truthy, timestr_to_secs, secs_to_timestr
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, WebDriverException
from http.cookies import SimpleCookie
from furl import furl
from typing import Dict, Callable, Any
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import FirefoxProfile
import wrapt
import re
import json
from time import time
from pathlib import Path


@wrapt.decorator
def log_wrapper(wrapped: Callable, instance: "SeleniumTestability", args: Any, kwargs: Any) -> Any:
    instance.logger.debug("{}({}) [ENTERING]".format(wrapped.__name__, ", ".join([argstr(args), kwargstr(kwargs)])))
    ret = wrapped(*args, **kwargs)
    instance.logger.debug("{}() [LEAVING]".format(wrapped.__name__))
    return ret


class SeleniumTestability(LibraryComponent):
    """
    SeleniumTestability is plugin for SeleniumLibrary that provides either manual or automatic waiting asyncronous events within SUT. This works by injecting small javascript snippets that can monitor the web application's state and when any supported events are happening within the sut, execution of SeleniumLibrary's keywords are blocked until timeout or those events are processed.

    On top of this, there are some more or less useful utilities for web application testing.

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

    == Parameters ==

    Plugin can take parameters when it is initialized. All of these values can be modified at runtim too with corresponding keywords. Here's a list of the parameters:
    ===  automatic_wait ===
    a truthy value, if SeleniumTestabily should automatically wait for sut to be in state that it can accept more actions.
    Can be enabled/disable at runtime.
    Defaults to True
    === timeout  ===
    Robot timestring, amount of time to wait for SUT to be in state that it can be safely interacted with.
    Can be set at runtime.
    Defaults to 30 seconds.
    === error_on_timeout ===
    A truthy value, if timeout does occur either in manual or automatic mode, this determines if error should be thrown that marks marks the exection as failure.
    Can be enabled/disabled at runtime.
    Defaults to True
    === automatic_injection ===
    A truthy value. User can choose if he wants to instrument the SUT manually with appropriate keywords (or even, if the SUT is instrumented at build time?) or should SeleniumTestability determinine if SUT has testability features and if not then inject & instrument it automatically.
    Can be enabled/disabled at runtime.
    Defaults to True

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

    = Currently supported Asyncronouse features =

    - setTimeout & setImmediate calls and wait for them.
    - fetch() call and wait for it to finish
    - XHR requests and wait for them to finish
    - CSS Animations and wait form them to finish
    - CSS Transitions and wait form them to finish
    - Viewport scrolling.

    *Do note* that catching css animations and transitions is browser dependant. In the past
    certain browsers did not implement these features as "the standard" would require.

    = Other functionality. =

    SeleniumTestability also provides other conveniance keywords that do not make sense to incorporate into
    SeleniumLibrary itself, mainly due to functionality not being in scope of SeleniumLibrary and Selenium
    python bindings. Do check the keyword documentation for up to date list of keywords.

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
        self.logger = get_logger("SeleniumTestability")
        self.logger.debug("__init__({},{},{},{},{})".format(ctx, automatic_wait, timeout, error_on_timeout, automatic_injection))
        self.el = ElementKeywords(ctx)
        self.CWD = abspath(dirname(__file__))
        self.js_bundle = join(self.CWD, "js", "testability.js")
        self.ctx.event_firing_webdriver = TestabilityListener
        self.ctx.testability_settings = {"testability": self}
        self.automatic_wait = is_truthy(automatic_wait)
        self.automatic_injection = is_truthy(automatic_injection)
        self.error_on_timeout = is_truthy(error_on_timeout)
        self.timeout = timeout  # type: ignore
        self.hidden_elements = {}  # type: Dict[str, str]
        self.browser_warn_shown = False
        self.empty_log_warn_shown = False
        self.ff_log_pos = {}  # type: Dict[str, int]
        self.testability_config = None  # type: OptionalDictType

    @log_wrapper
    def _inject_testability(self: "SeleniumTestability") -> None:
        """
        Injects SeleniumTestability javascript bindings into a current browser's current window. This should happen automatically vie SeleniumTestability's internal `Event Firing Webdriver` support but keyword is provided also.
        """

        if self.testability_config:
            self.ctx.driver.execute_script(JS_LOOKUP["testability_config"], self.testability_config)

        with open(self.js_bundle, "r") as f:
            buf = f.read()
            self.ctx.driver.execute_script("{};".format(buf))

    @log_wrapper
    @keyword
    def set_testability_config(self: "SeleniumTestability", config: Dict) -> None:
        """
        Sets configuration that is used by SUT.  `config` dictionary should can have following keys: `maxTimeout` and `blacklist`.

        Configuration has to be set before opening any browsers or before SUT is instrumented either automatically or manually.

        - `maxTimeout` affects affects javascript `setTimeout()` calls and what is the maximum timeout that should be observed and waited. Value is milliseconds and defaults to 5000
        - `blacklist` is array of dictionaries where each array element have 2 fields. `url` and `method`.  `url` should be a regular expression that matches the actual url or url of the Request object's url field.
        Do note that the regular expression should match what is actually passed to the async method - not the fully qualied url.

        Parameters:
        - ``config`` dictionary of testability.js config options.

        Example:

        | &{longfetch}=           | `Create Dictionary`   | url=.*longfetch.*            |  method=GET              |
        | @{blacklist}=           | `Create List`         | ${longfetch}                 |                          |
        | ${tc}=                  | `Create Dictionary`   | maxTimeout=5000              |  blacklist=${blacklist}  |
        | Set Testability Config  |  ${tc}                |                              |                          |
.
        """
        self.testability_config = config

    @log_wrapper
    @keyword
    def instrument_browser(self: "SeleniumTestability") -> None:
        """
        Instruments the current webpage for testability. This should happen automatically vie SeleniumTestability's internal `Event Firing Webdriver` support but keyword is provided also. Calls `Inject Testability` keyword automatically.
        """
        if not self.is_testability_installed():
            self._inject_testability()

    @log_wrapper
    @keyword
    def is_testability_installed(self: "SeleniumTestability") -> bool:
        """
        Returns True if testability api's are loaded and current browser/window is instrumented, False if not.
        """
        return self.ctx.driver.execute_script(JS_LOOKUP["is_installed"])

    @log_wrapper
    @keyword
    def wait_for_document_ready(self: "SeleniumTestability") -> None:
        """
        Explicit waits until document.readyState is complete.
        """
        self.ctx.driver.execute_async_script(JS_LOOKUP["wait_for_document_ready"])

    @log_wrapper
    @keyword
    def set_testability_automatic_wait(self: "SeleniumTestability", enabled: bool) -> None:
        """
        Sets the state to TestabilityListener if it should automically call `Wait For Testability Ready` when interactions are done.
        Parameters:
         - ``enabled`` state of automatic waits.
        """
        self.automatic_wait = enabled

    @log_wrapper
    @keyword
    def enable_testability_automatic_wait(self: "SeleniumTestability") -> None:
        """
        Enables TestabilityListener to call `Wait For Testability Ready` onn all interactions that are done.
        """
        self.set_testability_automatic_wait(True)

    @log_wrapper
    @keyword
    def disable_testability_automatic_wait(self: "SeleniumTestability") -> None:
        """
        Disables TestabilityListener to call `Wait For Testability Ready` onn all interactions that are done.
        """
        self.set_testability_automatic_wait(False)

    @log_wrapper
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
        local_timeout = self.timeout
        if timeout is not None:
            local_timeout = timestr_to_secs(timeout)
        local_error_on_timeout = self.error_on_timeout
        if error_on_timeout is not None:
            local_error_on_timeout = is_truthy(error_on_timeout)

        try:
            WebDriverWait(self.ctx.driver, local_timeout, 0.15, ignored_exceptions=[TimeoutException]).until(
                lambda x: self.ctx.driver.execute_async_script(JS_LOOKUP["wait_for_testability"])
            )
        except TimeoutException:
            if local_error_on_timeout:
                raise TimeoutException("Timed out waiting for testability ready callback to trigger.")
        except Exception as e:
            self.warn(e)

    @log_wrapper
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

    @log_wrapper
    @keyword
    def get_testability_timeout(self: "SeleniumTestability") -> str:
        """
        Returns the global timeout value in robot framework timestr format for waiting testability ready.
        """
        return secs_to_timestr(self.timeout)

    @log_wrapper
    @keyword
    def set_testability_error_on_timeout(self: "SeleniumTestability", error_on_timeout: bool) -> None:
        """Sets the global error_on_timeout value. eg, should SeleniumTestability throw exception when timeout occurs and there are still events in the testability queue.
        Parameters:
        - ``error_on_timeout``  - any value that robot framework considers truthy can be provided here.
        """
        self.error_on_timeout = error_on_timeout

    @keyword
    @log_wrapper
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

    @log_wrapper
    @keyword
    def set_testability_automatic_injection(self: "SeleniumTestability", enabled: bool) -> None:
        """
        Sets the state to TestabilityListener if it should automically inject testability.
        Parameters:
         - ``enabled`` state of automatic injection
        """
        self.automatic_injection = enabled

    @log_wrapper
    @keyword
    def enable_testability_automatic_injection(self: "SeleniumTestability") -> None:
        """
        Enables TestabilityListener to automatically inject testability.
        """
        self.set_testability_automatic_injection(True)

    @log_wrapper
    @keyword
    def disable_testability_automatic_injection(self: "SeleniumTestability") -> None:
        """
        Disables TestabilityListener to automatically inject testability
        """
        self.set_testability_automatic_injection(False)

    @staticmethod
    @keyword
    def cookies_to_dict(cookies: str) -> dict:  # FIX: cookies can be dict also
        """
        Converts a cookie string into python dict.
        """
        ret = {}
        cookie = SimpleCookie()  # type: SimpleCookie
        cookie.load(cookies)
        for key, morsel in cookie.items():
            ret[key] = morsel.value
        return ret

    @log_wrapper
    @keyword
    def get_navigator_useragent(self: "SeleniumTestability") -> str:
        """
        Returns useragent string of current browser.
        """
        return self.ctx.driver.execute_script(JS_LOOKUP["navigator"], "userAgent")

    @log_wrapper
    @keyword
    def get_navigator_appCodeName(self: "SeleniumTestability") -> str:
        """
        Returns appCoedName string of current browser.
        """
        return self.ctx.driver.execute_script(JS_LOOKUP["navigator"], "appCodeName")

    @log_wrapper
    @keyword
    def get_navigator_appname(self: "SeleniumTestability") -> str:
        """
        Returns appName string of current browser.
        """
        return self.ctx.driver.execute_script(JS_LOOKUP["navigator"], "appName")

    @log_wrapper
    @keyword
    def get_navigator_appversion(self: "SeleniumTestability") -> str:
        """
        Returns appVersion string of current browser.
        """
        return self.ctx.driver.execute_script(JS_LOOKUP["navigator"], "appVersion")

    @log_wrapper
    @keyword
    def get_navigator_cookieenabled(self: "SeleniumTestability") -> bool:
        """
        Returns cookieEnabled boolean of current browser.
        """
        return self.ctx.driver.execute_script(JS_LOOKUP["navigator"], "cookieEnabled")

    @log_wrapper
    @keyword
    def get_navigator_language(self: "SeleniumTestability") -> str:
        """
        Returns language string of current browser.
        """
        return self.ctx.driver.execute_script(JS_LOOKUP["navigator"], "language")

    @log_wrapper
    @keyword
    def get_navigator_online(self: "SeleniumTestability") -> bool:
        """
        Returns online boolean of current browser.
        """
        return self.ctx.driver.execute_script(JS_LOOKUP["navigator"], "onLine")

    @log_wrapper
    @keyword
    def get_navigator_platform(self: "SeleniumTestability") -> str:
        """
        Returns platform string of current browser.
        """
        return self.ctx.driver.execute_script(JS_LOOKUP["navigator"], "platform")

    @log_wrapper
    @keyword
    def get_navigator_product(self: "SeleniumTestability") -> str:
        """
        Returns product string of current browser.
        """
        return self.ctx.driver.execute_script(JS_LOOKUP["navigator"], "product")

    @log_wrapper
    @keyword
    def drag_and_drop(self: "SeleniumTestability", locator: LocatorType, target: LocatorType, html5: bool = False) -> None:
        """Drags element identified by ``locator`` into ``target`` element.

        The ``locator`` argument is the locator of the dragged element
        and the ``target`` is the locator of the target. See the
        `Locating elements` section for details about the locator syntax.

        If you wish to drag and drop a file from a local filesystem, you can specify the locator as `file:/full/path/to/filename`
        and SeleniumTestability will generate a drag'n'drop events to upload a file into a given `target` element.

        ``html5`` parameter is optional and if provided, `drag_and_drop`will utilize
        javascript to trigger the suitable events ensuring that html5 applications
        receive the right events. If `locator` starts with file: prefix, html5 defaults to True.

        Example:
        | `Drag And Drop` | css:div#element | css:div.target |  html5=True |
        | `Drag And Drop` | file:/home/rasjani/testfile.txt  |  id:demo-upload |
        """
        file_prefix = "file:"
        html5 = is_truthy(html5)
        if file_prefix in locator:
            html5 = True

        if not html5:
            self.el.drag_and_drop(locator, target)
        else:
            to_element = self.el.find_element(target)
            filename = None
            if type(locator) == str and file_prefix in locator:
                filename = locator[locator.startswith(file_prefix) and len(file_prefix):]

            if filename is not None:
                if Path(filename).exists():
                    file_input = self.driver.execute_script(JS_LOOKUP["drag_and_drop_file"], to_element, 0, 0)
                    file_input.send_keys(filename)
                else:
                    raise RuntimeError(f"Unable to upload {filename} - its missing")
            else:
                from_element = self.el.find_element(locator)
                self.ctx.driver.execute_script(JS_LOOKUP["dragdrop"], from_element, to_element)

    @log_wrapper
    @keyword
    def scroll_to_bottom(self: "SeleniumTestability", smooth: bool = False) -> None:
        """
        Scrolls current window to the bottom of the page
        Parameters:
         - ``smooth`` if sets to true, enables smooth scrolling, otherwise instant.
        """
        smooth = bool(smooth)
        behavior = "smooth" if smooth else "instant"
        self.ctx.driver.execute_script(JS_LOOKUP["scroll_to_bottom"], behavior)

    @log_wrapper
    @keyword
    def scroll_to_top(self: "SeleniumTestability", smooth: bool = False) -> None:
        """
        Scrolls current window to the top of the page
        Parameters:
         - ``smooth`` if sets to true, enables smooth scrolling, otherwise instant.
        """
        smooth = bool(smooth)
        behavior = "smooth" if smooth else "instant"
        self.ctx.driver.execute_script(JS_LOOKUP["scroll_to_top"], behavior)

    @log_wrapper
    @keyword
    def toggle_element_visibility(self: "SeleniumTestability", locator: LocatorType) -> None:
        """
        Toggles visiblity state of element via ``locator``
        """
        if locator in self.hidden_elements:
            self.hide_element(locator)
        else:
            self.show_element(locator)

    @log_wrapper
    @keyword
    def hide_element(self: "SeleniumTestability", locator: LocatorType) -> None:
        """
        Hides element via ``locator``. Typically one would use this to avoid getting
        Toggles visiblity state of element via ``locator``
        past overlays that are on top of element that is to be interacted with.
        """
        from_element = self.el.find_element(locator)
        current_display = self.ctx.driver.execute_script(JS_LOOKUP["get_style_display"], from_element)
        self.hidden_elements[locator] = current_display
        self.ctx.driver.execute_script(JS_LOOKUP["set_style_display"], from_element, "none")

    @log_wrapper
    @keyword
    def show_element(self: "SeleniumTestability", locator: LocatorType) -> None:
        """
        Shows element via ``locator`` that has been previously been hidden with `Hide Element` keyword.
        """
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

    @log_wrapper
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

    @log_wrapper
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

    @log_wrapper
    @keyword
    def element_should_be_blocked(self: "SeleniumTestability", locator: LocatorType) -> None:
        """
        Throws exception if element found with ``locator`` is not blocked by any overlays.
        Example:
        | Element Should Be Blocked  |  id:some_id |
        If nothing is on top of of provided element, throws an exception
        """
        is_blocked = self._element_blocked(locator)
        if not is_blocked:
            raise AssertionError("Element with locator {} is not blocked".format(locator))

    @log_wrapper
    @keyword
    def element_should_not_be_blocked(self: "SeleniumTestability", locator: LocatorType) -> None:
        """
        Throws exception if element found with ``locator`` is being blocked by overlays.
        Example:
        | Element Should Not Be Blocked  |  id:some_id |
        If there's element on top of provided selector, throws an exception
        """
        is_blocked = self._element_blocked(locator)
        if is_blocked:
            raise AssertionError("Element with locator {} is blocked".format(locator))

    def _get_ff_log(self: "SeleniumTestability", name: str) -> BrowserLogsType:
        matcher = (
            r"^(?P<source>JavaScript|console)(\s|\.)(?P<level>warn.*?|debug|trace|log|error|info):\s(?P<message>(?!resource:).*)$"
        )
        LEVEL_LOOKUP = {
            "log": "INFO",
            "warn": "WARN",
            "warning": "WARN",
            "error": "SEVERE",
            "info": "INFO",
            "trace": "SEVERE",
            "debug": "DEBUG",
        }
        SOURCE_LOOKUP = {"JavaScript": "javascript", "console": "console-api"}
        log = []
        skip_lines = self.ff_log_pos.get(name, 0)
        buff: BrowserLogsType = []
        with open(name, "r") as f:
            buff = f.read().split("\n")
        self.ff_log_pos[name] = skip_lines + len(buff)
        buff = buff[skip_lines:]

        for line in buff:
            matches = re.search(matcher, line)
            if matches:
                row = {
                    "level": LEVEL_LOOKUP[matches.group("level")],
                    "message": matches.group("message"),
                    "source": SOURCE_LOOKUP[matches.group("source")],
                    "timestamp": int(time() * 1000),
                }
                log.append(json.dumps(row))
        return log

    @log_wrapper
    @keyword
    def get_log(self: "SeleniumTestability", log_type: str = "browser") -> BrowserLogsType:
        """
        Returns logs determined by ``log_type`` from the current browser. What is returned
        depends on desired_capabilities passed to `Open Browser`.

        Note: On firefox, the firefox profile has to have `devtools.console.stdout.content` property to be set.
        This can be done automatically with `Generate Firefox Profile` and then pass that to `Open Browser`.

        This keyword will mostly likely not work with remote seleniun driver!
        """
        ret = []  # type: BrowserLogsType
        try:
            if is_firefox(self.ctx.driver) and log_type == "browser":
                ret = self._get_ff_log(self.ctx.driver.service.log_file.name)
            else:
                ret = self.ctx.driver.get_log(log_type)
        except WebDriverException:
            if not self.browser_warn_shown:
                self.browser_warn_shown = True
                self.warn("Current browser does not support fetching logs from the browser with log_type: {}".format(log_type))
                return []
        if not ret and not self.empty_log_warn_shown:
            self.empty_log_warn_shown = True
            self.warn("No logs available - you might need to enable loggingPrefs in desired_capabilities")
        return ret

    @log_wrapper
    @keyword
    def get_default_capabilities(self: "SeleniumTestability", browser_name: str) -> OptionalDictType:
        """
        Returns a set of default capabilities for given ``browser``.
        """
        try:
            browser = browser_name.lower().replace(" ", "")
            return self.BROWSERS[browser].copy()
        except Exception as e:
            self.logger.debug(e)
            return None

    @log_wrapper
    @keyword
    def set_element_attribute(self: "SeleniumTestability", locator: LocatorType, attribute: str, value: str) -> None:
        """
        Sets ``locator`` attribute ``attribute`` to ``value``
        """
        from_element = self.el.find_element(locator)
        self.ctx.driver.execute_script(JS_LOOKUP["set_element_attribute"], from_element, attribute, value)

    @log_wrapper
    @keyword
    def get_location_hash(self: "SeleniumTestability") -> str:
        """
        returns the fragment identifier of the URL prefexed by a '#'
        """
        return self.ctx.driver.execute_script(JS_LOOKUP["get_window_location"], "hash")

    @log_wrapper
    @keyword
    def get_location_host(self: "SeleniumTestability") -> str:
        """
        returns the hostname and the port of the URL appended by a ':'
        """
        return self.ctx.driver.execute_script(JS_LOOKUP["get_window_location"], "host")

    @log_wrapper
    @keyword
    def get_location_hostname(self: "SeleniumTestability") -> str:
        """
        return the hostname of the URL
        """
        return self.ctx.driver.execute_script(JS_LOOKUP["get_window_location"], "hostname")

    @log_wrapper
    @keyword
    def get_location_href(self: "SeleniumTestability") -> str:
        """
        returns the entire URL
        """
        return self.ctx.driver.execute_script(JS_LOOKUP["get_window_location"], "href")

    @log_wrapper
    @keyword
    def get_location_origin(self: "SeleniumTestability") -> str:
        """
        returns the canonical form of the origin of the specific location
        """
        return self.ctx.driver.execute_script(JS_LOOKUP["get_window_location"], "origin")

    @log_wrapper
    @keyword
    def get_location_port(self: "SeleniumTestability") -> str:
        """
        returns the port number of the URL
        """
        return self.ctx.driver.execute_script(JS_LOOKUP["get_window_location"], "port")

    @log_wrapper
    @keyword
    def get_location_protocol(self: "SeleniumTestability") -> str:
        """
        returns the protocol scheme of the URL
        """
        return self.ctx.driver.execute_script(JS_LOOKUP["get_window_location"], "protocol")

    @log_wrapper
    @keyword
    def get_location_search(self: "SeleniumTestability") -> str:
        """
        returns the sting containing a '?' followed by the parameters or ``querystring`` of the URL
        """
        return self.ctx.driver.execute_script(JS_LOOKUP["get_window_location"], "search")

    @log_wrapper
    @keyword
    def generate_firefox_profile(
        self: "SeleniumTestability",
        preferences: OptionalDictType = None,
        accept_untrusted_certs: bool = False,
        proxy: OptionalStrType = None,
    ) -> FirefoxProfile:
        """
        Generates a firefox profile that sets up few required preferences for SeleniumTestability to support all necessary features.
        Parameters:
        - ``preferences`` - firefox profile preferences in dictionary format.
        - ``accept_untrusted_certs`` should we accept untrusted/self-signed certificates.
        - ``proxy`` proxy options

        Note: If you opt out using this keyword, you are not able to get logs with ``Get Logs`` and Firefox.
        """
        profile = FirefoxProfile()
        if preferences:
            for key, value in preferences.items():  # type: ignore
                profile.set_preference(key, value)

        profile.set_preference("devtools.console.stdout.content", True)

        profile.accept_untrusted_certs = accept_untrusted_certs

        if proxy:
            profile.set_proxy(proxy)

        profile.update_preferences()
        return profile

    @log_wrapper
    @keyword
    def get_storage_length(self: "SeleniumTestability", storage_type: str = "localStorage") -> int:
        """
        Returns a length (# of items) in specified storage.
        Parameters:
        - ``storage_type`` name of the storage. Valid options: localStorage, sessionStorage
        """
        return self.ctx.driver.execute_script(JS_LOOKUP["storage_length"], storage_type)

    @log_wrapper
    @keyword
    def get_storage_keys(self: "SeleniumTestability", storage_type: str = "localStorage") -> StringArray:
        """
        Returns a list of keys in specified storage.
        Parameters:
        - ``storage_type`` name of the storage. Valid options: localStorage, sessionStorage
        """
        return self.ctx.driver.execute_script(JS_LOOKUP["storage_keys"], storage_type)

    @log_wrapper
    @keyword
    def get_storage_item(self: "SeleniumTestability", key: str, storage_type: str = "localStorage") -> StorageType:
        """
        Returns value of ``key`` from specified storage.
        Parameters:
        - ``key`` name of the storage key
        - ``storage_type`` name of the storage. Valid options: localStorage, sessionStorage
        """
        matcher = r"^{.*}$"
        storage_item = self.ctx.driver.execute_script(JS_LOOKUP["storage_getitem"], storage_type, key)
        if isinstance(storage_item, str) and re.match(matcher, storage_item):
            storage_item = json.loads(storage_item)
        return storage_item

    @log_wrapper
    @keyword
    def set_storage_item(self: "SeleniumTestability", key: str, value: StorageType, storage_type: str = "localStorage") -> None:
        """
        Sets a value to the key in specified storage_type
        Parameters:
        - ``key`` name of the key
        - ``value`` value that should be set to key
        - ``storage_type`` name of the storage. Valid options: localStorage, sessionStorage
        """
        if isinstance(value, dict):
            value = json.dumps(value)
        self.ctx.driver.execute_script(JS_LOOKUP["storage_setitem"], storage_type, key, value)

    @log_wrapper
    @keyword
    def clear_storage(self: "SeleniumTestability", storage_type: str = "localStorage") -> None:
        """
        Clears all values in specified storage.
        Parameters:
        - ``storage_type`` name of the storage. Valid options: localStorage, sessionStorage
        """
        self.ctx.driver.execute_script(JS_LOOKUP["storage_clear"], storage_type)

    @log_wrapper
    @keyword
    def remove_storage_item(self: "SeleniumTestability", key: str, storage_type: str = "localStorage") -> None:
        """
        Removes a key and its value from specified storage
        Parameters:
        - ``key`` name of the key
        - ``storage_type`` name of the storage. Valid options: localStorage, sessionStorage
        """
        return self.ctx.driver.execute_script(JS_LOOKUP["storage_removeitem"], storage_type, key)

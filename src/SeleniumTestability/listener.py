# -*- coding: utf-8 -*-
from SeleniumLibrary import SeleniumLibrary
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.events import AbstractEventListener
from robot.libraries.BuiltIn import BuiltIn
from .logger import get_logger, kwargstr, argstr
import wrapt
from typing import Callable, Any


@wrapt.decorator
def log_wrapper(wrapped: Callable, instance: "TestabilityListener", args: Any, kwargs: Any) -> None:
    instance.logger.debug("{}({}) [ENTERING]".format(wrapped.__name__, ", ".join([argstr(args), kwargstr(kwargs)])))
    wrapped(*args, **kwargs)
    instance.logger.debug("{}() [LEAVING]".format(wrapped.__name__))


def auto_injection(func: Callable) -> Callable:
    def injection_wrapper(*args: Any, **kwargs: Any) -> Any:
        this = args[0]
        if this.automatic_injection:
            this.testability.instrument_browser()
        return func(*args, **kwargs)

    return injection_wrapper


class TestabilityListener(AbstractEventListener):
    @property
    def automatic_wait(self: "TestabilityListener") -> bool:
        return self.testability.testability_settings["automatic_wait"]

    @property
    def automatic_injection(self: "TestabilityListener") -> bool:
        return self.testability.testability_settings["automatic_injection"]

    def __init__(self: "TestabilityListener") -> None:
        AbstractEventListener.__init__(self)
        self.testability = self._get_sl()
        self.logger = get_logger("TestabilityListener")
        self.logger.debug("__init__()")

    def _get_sl(self: "TestabilityListener") -> SeleniumLibrary:
        libraries = BuiltIn().get_library_instance(all=True)
        for library in libraries:
            if isinstance(libraries[library], SeleniumLibrary):
                return libraries[library]
        return None

    @log_wrapper
    def before_navigate_to(self: "TestabilityListener", url: str, driver: WebDriver) -> None:
        pass

    @log_wrapper
    @auto_injection
    def after_navigate_to(self: "TestabilityListener", url: str, driver: WebDriver) -> None:
        pass

    @log_wrapper
    @auto_injection
    def before_click(self: "TestabilityListener", element: WebElement, driver: WebDriver) -> None:
        pass

    @log_wrapper
    def after_click(self: "TestabilityListener", element: WebElement, driver: WebDriver) -> None:
        pass

    @log_wrapper
    @auto_injection
    def before_change_value_of(self: "TestabilityListener", element: WebElement, driver: WebDriver) -> None:
        pass

    @log_wrapper
    def after_change_value_of(self: "TestabilityListener", element: WebElement, driver: WebDriver) -> None:
        pass

    @log_wrapper
    def after_close(self: "TestabilityListener", driver: WebDriver) -> None:
        pass

    @log_wrapper
    def after_execute_script(self: "TestabilityListener", script: str, driver: WebDriver) -> None:
        pass

    @log_wrapper
    def after_find(self: "TestabilityListener", by: str, value: str, driver: WebDriver) -> None:
        pass

    @log_wrapper
    @auto_injection
    def after_navigate_back(self: "TestabilityListener", driver: WebDriver) -> None:
        pass

    @log_wrapper
    @auto_injection
    def after_navigate_forward(self: "TestabilityListener", driver: WebDriver) -> None:
        pass

    @log_wrapper
    def after_quit(self: "TestabilityListener", driver: WebDriver) -> None:
        pass

    @log_wrapper
    def before_close(self: "TestabilityListener", driver: WebDriver) -> None:
        pass

    @log_wrapper
    def before_execute_script(self: "TestabilityListener", script: str, driver: WebDriver) -> None:
        pass

    @log_wrapper
    @auto_injection
    def before_find(self: "TestabilityListener", by: str, value: str, driver: WebDriver) -> None:
        if self.automatic_wait:
            self.testability.wait_for_testability_ready()

    @log_wrapper
    def before_navigate_back(self: "TestabilityListener", driver: WebDriver) -> None:
        pass

    @log_wrapper
    def before_navigate_forward(self: "TestabilityListener", driver: WebDriver) -> None:
        pass

    @log_wrapper
    def before_quit(self: "TestabilityListener", driver: WebDriver) -> None:
        pass

    @log_wrapper
    def on_exception(self: "TestabilityListener", exception: Exception, driver: WebDriver) -> None:
        self.logger.warn(str(exception))

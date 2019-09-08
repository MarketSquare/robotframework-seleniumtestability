# -*- coding: utf-8 -*-
from SeleniumLibrary import SeleniumLibrary
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from robot.api import logger
from selenium.webdriver.support.events import AbstractEventListener
from robot.libraries.BuiltIn import BuiltIn


class TestabilityListener(AbstractEventListener):
    @property
    def automatic_wait(self: "TestabilityListener") -> bool:
        return self.testability.testability_settings["automatic_wait"]

    @property
    def automatic_injection(self: "TestabilityListener") -> bool:
        return self.testability.testability_settings["automatic_injection"]

    def __init__(self: "TestabilityListener") -> None:
        self.testability = self._get_sl()

    def _get_sl(self: "TestabilityListener") -> SeleniumLibrary:
        libraries = BuiltIn().get_library_instance(all=True)
        for library in libraries:
            if isinstance(libraries[library], SeleniumLibrary):
                return libraries[library]
        return None

    def before_navigate_to(self: "TestabilityListener", url: str, driver: WebDriver) -> None:
        logger.debug("TestabilityListener: before_navigate_to(%s, %s)" % (url, driver))

    def after_navigate_to(self: "TestabilityListener", url: str, driver: WebDriver) -> None:
        logger.debug("TestabilityListener: after_navigate_to(%s, %s)" % (url, driver))
        if self.automatic_injection:
            self.testability.instrument_browser()

    def before_click(self: "TestabilityListener", element: WebElement, driver: WebDriver) -> None:
        logger.debug("TestabilityListener: before_click(%s, %s)" % (element, driver))
        if self.automatic_wait:
            self.testability.wait_for_testability_ready()

    def after_click(self: "TestabilityListener", element: WebElement, driver: WebDriver) -> None:
        logger.debug("TestabilityListener: after_click(%s, %s)" % (element, driver))

    def before_change_value_of(self: "TestabilityListener", element: WebElement, driver: WebDriver) -> None:
        logger.debug("TestabilityListener: before_change_value_of(%s, %s)" % (element, driver))
        if self.automatic_wait:
            self.testability.wait_for_testability_ready()

    def after_change_value_of(self: "TestabilityListener", element: WebElement, driver: WebDriver) -> None:
        logger.debug("TestabilityListener: after_change_value_of(%s, %s)" % (element, driver))

    def after_close(self: "TestabilityListener", driver: WebDriver) -> None:
        logger.debug("TestabilityListener: after_close(%s)" % driver)

    def after_execute_script(self: "TestabilityListener", script: str, driver: WebDriver) -> None:
        logger.debug("TestabilityListener: after_execute_script(%s, %s)" % (script, driver))

    def after_find(self: "TestabilityListener", by: str, value: str, driver: WebDriver) -> None:
        logger.debug("TestabilityListener: after_find(%s, %s, %s)" % (by, value, driver))

    def after_navigate_back(self: "TestabilityListener", driver: WebDriver) -> None:
        logger.debug("TestabilityListener: after_navigate_back(%s)" % driver)
        if self.automatic_injection:
            self.testability.instrument_browser()

    def after_navigate_forward(self: "TestabilityListener", driver: WebDriver) -> None:
        logger.debug("TestabilityListener: after_navigate_forward(%s)" % driver)
        if self.automatic_injection:
            self.testability.instrument_browser()

    def after_quit(self: "TestabilityListener", driver: WebDriver) -> None:
        logger.debug("TestabilityListener: after_quit(%s)" % driver)

    def before_close(self: "TestabilityListener", driver: WebDriver) -> None:
        logger.debug("TestabilityListener: before_close(%s)" % driver)

    def before_execute_script(self: "TestabilityListener", script: str, driver: WebDriver) -> None:
        logger.debug("TestabilityListener: before_execute_script(%s,%s) " % (script, driver))

    def before_find(self: "TestabilityListener", by: str, value: str, driver: WebDriver) -> None:
        logger.debug("TestabilityListener: before_find(%s, %s, %s)" % (by, value, driver))
        if self.automatic_injection:
            self.testability.instrument_browser()
        if self.automatic_wait:
            self.testability.wait_for_testability_ready()

    def before_navigate_back(self: "TestabilityListener", driver: WebDriver) -> None:
        logger.debug("TestabilityListener: before_navigate_back(%s)" % driver)

    def before_navigate_forward(self: "TestabilityListener", driver: WebDriver) -> None:
        logger.debug("TestabilityListener: before_navigate_forward(%s)" % driver)

    def before_quit(self: "TestabilityListener", driver: WebDriver) -> None:
        logger.debug("TestabilityListener: before_quit(%s)" % driver)

    def on_exception(self: "TestabilityListener", exception: Exception, driver: WebDriver) -> None:
        logger.debug("TestabilityListener: on_exception(%s, %s)" % (exception, driver))

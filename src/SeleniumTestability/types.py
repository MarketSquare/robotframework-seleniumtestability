# -*- coding: utf-8 -*-
from typing import Union, Optional, List
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebElement, EventFiringWebDriver
from selenium.webdriver import Firefox
from selenium.webdriver.remote.webelement import WebElement
from psutil import Process

WebElementType = Union[WebElement, EventFiringWebElement]
LocatorType = Union[WebElementType, EventFiringWebElement, str]
OptionalBoolType = Optional[bool]
OptionalStrType = Optional[str]
OptionalDictType = Optional[str]
BrowserLogsType = List[str]
ProcessType = Union[Process, int]
FirefoxWebDriverType = Union[Firefox, EventFiringWebDriver]


def is_firefox(webdriver: FirefoxWebDriverType) -> bool:
    if isinstance(webdriver, Firefox):
        return True
    if isinstance(webdriver, EventFiringWebDriver):
        if isinstance(webdriver.wrapped_driver, Firefox):
            return True
    return False

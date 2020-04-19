# -*- coding: utf-8 -*-
from typing import Union, Optional, List, Dict
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebElement, EventFiringWebDriver
from selenium.webdriver import Firefox
from selenium.webdriver.remote.webelement import WebElement

try:
    # Only required during development.
    from psutil import Process

    ProcessType = Union[Process, int]
except ModuleNotFoundError:
    pass

WebElementType = Union[WebElement, EventFiringWebElement]
LocatorType = Union[WebElementType, EventFiringWebElement, str]
OptionalBoolType = Optional[bool]
OptionalStrType = Optional[str]
OptionalDictType = Optional[Dict]
BrowserLogsType = List[str]
StringArray = List[str]
FirefoxWebDriverType = Union[Firefox, EventFiringWebDriver]
StorageType = Union[Dict, bool, str, int, float]


def is_firefox(webdriver: FirefoxWebDriverType) -> bool:
    if isinstance(webdriver, Firefox):
        return True
    if isinstance(webdriver, EventFiringWebDriver):
        if isinstance(webdriver.wrapped_driver, Firefox):
            return True
    return False

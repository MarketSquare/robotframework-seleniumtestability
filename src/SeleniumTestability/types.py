# -*- coding: utf-8 -*-
from typing import Union, Optional, List
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebElement
from selenium.webdriver.remote.webelement import WebElement
from psutil import Process

WebElementType = Union[WebElement, EventFiringWebElement]
LocatorType = Union[WebElementType, EventFiringWebElement, str]
OptionalBoolType = Optional[bool]
OptionalStrType = Optional[str]
OptionalDictType = Optional[str]
BrowserLogsType = List[str]
ProcessType = Union[Process, int]

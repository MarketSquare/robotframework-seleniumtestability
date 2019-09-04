from typing import Union, Optional
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebElement
from selenium.webdriver.remote.webelement import WebElement

WebElementType = Union[WebElement, EventFiringWebElement]
LocatorType = Union[WebElementType, EventFiringWebElement, str]
OptionalBoolType = Optional[bool]
OptionalStrType = Optional[str]

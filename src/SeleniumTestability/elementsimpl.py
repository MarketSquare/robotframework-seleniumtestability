# -*- coding: utf-8 -*-
from .utils import log_wrapper
from .javascript import JS_LOOKUP
from SeleniumLibrary.base import keyword
from .types import (
    WebElementType,
    LocatorType,
)


class SeleniumTestability:
    pass


class ElementsMixin:
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

    @log_wrapper
    @keyword
    def set_element_attribute(self: "SeleniumTestability", locator: LocatorType, attribute: str, value: str) -> None:
        """
        Sets ``locator`` attribute ``attribute`` to ``value``
        """
        from_element = self.el.find_element(locator)
        self.ctx.driver.execute_script(JS_LOOKUP["set_element_attribute"], from_element, attribute, value)

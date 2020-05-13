# -*- coding: utf-8 -*-
from .utils import log_wrapper
from .javascript import JS_LOOKUP
from SeleniumLibrary.base import keyword


class SeleniumTestability:
    pass


class NavigatorMixin:

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

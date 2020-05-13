# -*- coding: utf-8 -*-
from .utils import log_wrapper
from .javascript import JS_LOOKUP
from SeleniumLibrary.base import keyword


class SeleniumTestability:
    pass


class LocationMixin:
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

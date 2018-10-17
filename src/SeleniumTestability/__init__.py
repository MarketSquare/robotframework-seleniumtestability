#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from robot.api import logger
from time import sleep
from robot.libraries.BuiltIn import BuiltIn
from SeleniumLibrary import SeleniumLibrary
from SeleniumLibrary.base import keyword
from SeleniumLibrary.keywords import JavaScriptKeywords

from os.path import abspath, dirname

class SeleniumTestability(SeleniumLibrary):
    def run_keyword(self, name, args, kwargs):
        logger.warn("run_keyword: {} {} {}".format(name,args,kwargs))
        if name == "click_element":
            self.wait_for_testability_ready()
        SeleniumLibrary.run_keyword(self, name, args, kwargs)

    @keyword
    def inject_testability(self):
        js = JavaScriptKeywords(self)
        base_path = dirname(abspath(__file__))
        with open("{}/testability/api_inject.js".format(base_path),'r') as f:
            buf = f.read()
            res = js.execute_javascript(buf)
            js.execute_javascript("{}; window.testability = testability;".format(buf));

        with open("{}/testability/bindings.js".format(base_path),'r') as f:
            buf = f.read()
            js.execute_javascript("{}; window.instrumentBrowser = instrumentBrowser;".format(buf));
            res = js.execute_javascript(buf)


    @keyword
    def instrument_browser(self):
        js = JavaScriptKeywords(self)
        js.execute_javascript("window.instrumentBrowser(window)")

    @keyword
    def wait_for_testability_ready(self):
        # TODO: Feels dirty to get instance every time, fix later
        js = JavaScriptKeywords(self)
        js.execute_async_javascript("var cb = arguments[arguments.length - 1]; window.testability.when.ready(function() {cb()});")


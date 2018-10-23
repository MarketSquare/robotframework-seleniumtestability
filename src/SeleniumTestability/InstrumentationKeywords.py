# -*- coding: utf-8 -*-

from SeleniumLibrary.base import keyword, LibraryComponent
from SeleniumLibrary.keywords import JavaScriptKeywords
from os.path import abspath, dirname


def get_base_path():
    return dirname(abspath(__file__))


class InstrumentationKeywords(LibraryComponent):
    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)
        self.js_keywords = JavaScriptKeywords(self.ctx)
        self.base_path = get_base_path()

    @keyword
    def inject_testability(self):
        with open("{}/testability/api_inject.js".format(self.base_path), 'r') as f:
            buf = f.read()
            self.js_keywords.execute_javascript("{}; window.testability = testability;".format(buf))

        with open("{}/testability/bindings.js".format(self.base_path), 'r') as f:
            buf = f.read()
            self.js_keywords.execute_javascript("{}; window.instrumentBrowser = instrumentBrowser;".format(buf))

    @keyword
    def instrument_browser(self):
        js = JavaScriptKeywords(self)
        js.execute_javascript("window.instrumentBrowser(window)")

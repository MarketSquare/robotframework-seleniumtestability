# -*- coding: utf-8 -*-

from SeleniumLibrary.base import keyword, LibraryComponent
from SeleniumLibrary.keywords import JavaScriptKeywords
from os.path import abspath, dirname


def get_base_path():
    return dirname(abspath(__file__))


class WaitForTestabilityKeyword(LibraryComponent):

    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)
        self.js_keywords = JavaScriptKeywords(self.ctx)
        self.base_path = get_base_path()

    @keyword
    def wait_for_testability_ready(self):
        """
        TODO: Wait For Testability Ready keyword
        """
        self.js_keywords.execute_async_javascript("var readyCallback = arguments[arguments.length - 1]; window.testability.when.ready(function() {readyCallback()});")

    @keyword
    def wait_for_document_ready(self):
        """
        TODO: Wait For Document Ready keyword
        """
        self.js_keywords.execute_async_javascript("var readyCallback = arguments[arguments.length - 1]; var checkReadyState=function() { document.readyState !== 'complete' ?  setTimeout(checkReadyState, 11) : readyCallback();}; checkReadyState()")

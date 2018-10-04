from robot.api import logger
from time import sleep
from robot.libraries.BuiltIn import BuiltIn
from SeleniumLibrary import SeleniumLibrary
from SeleniumLibrary.base import keyword
from SeleniumLibrary.keywords import JavaScriptKeywords


class TestabilityLibrary(SeleniumLibrary):
    def run_keyword(self, name, args, kwargs):
        logger.warn("run_keyword: {} {} {}".format(name,args,kwargs))
        if name == "click_element":
            self.wait_for_testability_ready()
        SeleniumLibrary.run_keyword(self, name, args, kwargs)

    def find_elements(self, locator, parent=None):
        logger.warn("find_elements: {}".format(locator))
        SeleniumLibrary.find_elements(self, locator, parent)

    def find_element(self, locator, parent=None):
        logger.warn("find_element: {}".format(locator))
        SeleniumLibrary.find_element(self, locator, parent)

    @keyword
    def inject_testability(self):
        js = JavaScriptKeywords(self)
        exec_path = BuiltIn().get_variable_value("${EXEC_DIR}")
        with open("{}/www/api_inject.js".format(exec_path),'r') as f:
            buf = f.read()
            res = js.execute_javascript(buf)
            js.execute_javascript("{}; window.testability = testability;".format(buf));

        with open("{}/www/bindings.js".format(exec_path),'r') as f:
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


# -*- coding: utf-8 -*-

from robot.libraries.BuiltIn import BuiltIn
from SeleniumLibrary import SeleniumLibrary
from SeleniumLibrary.base import keyword

from .WaitForTestabilityKeyword import WaitForTestabilityKeyword
from .InstrumentationKeywords import InstrumentationKeywords


class SeleniumTestability(SeleniumLibrary):
    """
    = SeleniumTestability Library =
    SeleniumTestability is extension library for SeleniumLibrary that provides
    either manual or automatic waiting asyncronous events within SUT.

    This is accomplished by utilizing following 2 libraries. First one provides
    API and second one provides bindings.

    - https://github.com/alfonso-presa/testability.js
    - https://github.com/alfonso-presa/testability-browser-bindings

    When the SUT has been instrumented for testability, library provides a
    keyword that user can call in the testcode that prevents execution of
    seleniun keyword until the state of the SUT allows it. Alternatively,
    depending on how the the library has initialized, this waiting can happen
    automatically so that there is no extra code required from test code
    itself.

    == Usage ==

    == Instrumentation ==
    TODO
    ==  Waiting ==
    === Explicit ===
    TODO
    === Implicit Waiting ===
    TODO

    """

    def __init__(self, timeout=5.0, implicit_wait=0.0,
                 run_on_failure='Capture Page Screenshot',
                 screenshot_root_directory=None,
                 wait_testability=False
                 ):

        SeleniumLibrary.__init__(self, timeout=timeout, implicit_wait=implicit_wait,
                                 run_on_failure=run_on_failure,
                                 screenshot_root_directory=screenshot_root_directory)
        components = [WaitForTestabilityKeyword(self),
                      InstrumentationKeywords(self)]
        self.add_library_components(components)
        self.old_run_keyword = None
        if wait_testability:
            self.patch_run_keyword(wait_testability)
        # TODO:  Not a good way to go but lets start with this
        self.safe_keywords = ['add_cookie', 'add_location_strategy', 'close_all_browsers', 'close_browser', 'close_window', 'create_webdriver', 'get_selenium_implicit_wait', 'get_selenium_speed', 'get_selenium_timeout', 'get_session_id', 'get_source', 'get_window_handles', 'get_window_identifiers', 'get_window_names', 'get_window_position', 'get_window_size', 'get_window_titles', 'list_windows', 'log_location', 'log_source', 'log_title', 'maximize_browser_window', 'open_browser', 'patch_run_keyword', 'remove_location_strategy', 'restore_run_keyword', 'select_window', 'set_browser_implicit_wait', 'set_screenshot_directory', 'set_selenium_implicit_wait', 'set_selenium_speed', 'set_selenium_timeout', 'set_window_position', 'set_window_size', 'switch_browser', 'wait_for_testability_ready']

    def _force_reload(self):
        BuiltIn().reload_library("SeleniumTestability")

    @keyword
    def restore_run_keyword(self):
        """
        TODO: Restore Run Keywords docs
        """
        if self.old_run_keyword:
            self.run_keyword = self.old_run_keyword
            self.old_run_keyword = None
            self._force_reload()

    @keyword
    def patch_run_keyword(self, wait_testability=False):
        """
        TODO: Patch Run Keywords docs
        """
        if not self.old_run_keyword:
            self.old_run_keyword = self.run_keyword
            self.run_keyword = self.testability_run_keyword
            if not wait_testability:
                self._force_reload()

    def testability_run_keyword(self, name, args, kwargs):
        if name not in self.safe_keywords:
            self.wait_for_testability_ready()
        rk = self.old_run_keyword or self.run_keyword
        rk(name, args, kwargs)

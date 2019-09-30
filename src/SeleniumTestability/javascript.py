# -*- coding: utf-8 -*-
JS_LOOKUP = {
    "wait_for_testability": """
        var readyCallback = arguments[arguments.length - 1];
        window.testability.when.ready(function() {
            readyCallback(true)
        });
    """,
    "wait_for_document_ready": """
        var readyCallback = arguments[arguments.length - 1];
        var checkReadyState=function() {
            document.readyState !== 'complete' ?  setTimeout(checkReadyState, 50) : readyCallback(true);
        };
        checkReadyState();
    """,
    "is_installed": """
        return window.seleniumtestabilityready !== undefined && window.seleniumtestabilityready == true
    """,
    "navigator": """
        return navigator[arguments[0]]
    """,
    "dragdrop": """
        window.simulateDragDrop(arguments[0], arguments[1]);
    """,
    "scroll_to_bottom": """
        window.scrollTo(0, document.body.scrollHeight);
    """,
    "scroll_to_top": """
        window.scrollTo(0, 0);
    """,
    "get_style_display": """
        return arguments[0].style.display
    """,
    "set_style_display": """
        arguments[0].style.display = arguments[1]
    """,
    "get_rect": """
        return arguments[0].getBoundingClientRect()
    """,
    "get_element_at": """
        return document.elementFromPoint(arguments[0], arguments[1])
    """,
    "set_element_attribute": """
        arguments[0].setAttribute(arguments[1], arguments[2])
    """,
    "get_window_location": """
        return window.location[arguments[0]]
    """,
    "storage_getitem": """
        return window[arguments[0]].getItem(arguments[1])
    """,
    "storage_setitem": """
        window[arguments[0]].setItem(arguments[1], arguments[2])
    """,
    "storage_length": """
        return window[arguments[0]].length
    """,
    "storage_removeitem": """
        return window[arguments[0]].removeItem(arguments[1])
    """,
    "storage_clear": """
        return window[arguments[0]].clear()
    """,
    "storage_keys": """
        return Object.keys(window[arguments[0]])
    """,
}

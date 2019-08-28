
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

    "instrument_browser": """
        window.instrumentBrowser(window)
    """,

    "is_installed": """
        return window.testability !== undefined && window.instrumentBrowser !== undefined
    """,

    "useragent": """
        return navigator.userAgent;
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
}

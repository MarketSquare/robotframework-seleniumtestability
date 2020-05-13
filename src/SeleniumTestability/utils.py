# -*- coding: utf-8 -*-
import wrapt
from typing import Callable, Any


class SeleniumTestability:
    pass


def kwargstr(kwargs: Any) -> str:
    return ", ".join("%s=%r" % x for x in kwargs.items())


def argstr(args: Any) -> str:
    return ", ".join("%s" % x for x in args)


@wrapt.decorator
def log_wrapper(wrapped: Callable, instance: "SeleniumTestability", args: Any, kwargs: Any) -> Any:
    instance.logger.debug("{}({}) [ENTERING]".format(wrapped.__name__, ", ".join([argstr(args), kwargstr(kwargs)])))
    ret = wrapped(*args, **kwargs)
    instance.logger.debug("{}() [LEAVING]".format(wrapped.__name__))
    return ret

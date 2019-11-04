# -*- coding: utf-8 -*-
import logging
import os.path
from functools import lru_cache
from typing import Any
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError


def get_variable_from_robot(variable_name: str, default_value: Any) -> Any:
    try:
        return BuiltIn().get_variable_value("${{{}}}".format(variable_name))
    except RobotNotRunningError:
        return default_value


location = get_variable_from_robot("OUTPUT DIR", ".")
robot_log_level = get_variable_from_robot("LOG LEVEL", "INFO")
log_name = os.path.join(location, "{}.log".format("SeleniumTestability"))
log_handler = logging.FileHandler(log_name)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log_handler.setFormatter(formatter)
LEVELS = {"FAIL": logging.DEBUG, "WARN": logging.warn, "INFO": logging.INFO, "DEBUG": logging.debug, "TRACE": logging.DEBUG}


@lru_cache(maxsize=1)
def get_logger(name: str) -> Any:
    lgr = logging.getLogger(name)
    lgr.addHandler(log_handler)
    set_to = LEVELS.get(robot_log_level, logging.INFO)
    lgr.setLevel(set_to)  # type: ignore
    lgr.debug(" **** New Session Created for {}  **** ".format(name))
    return lgr


def kwargstr(kwargs: Any) -> str:
    return ", ".join("%s=%r" % x for x in kwargs.items())


def argstr(args: Any) -> str:
    return ", ".join("%s" % x for x in args)

# -*- coding: utf-8 -*-
import logging
from pathlib import Path
from functools import lru_cache
from typing import Any
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError

try:
    location = Path(BuiltIn().get_variable_value("${OUTPUT DIR}"))
    robot_log_level = BuiltIn().get_variable_value("${LOG LEVEL}")
except RobotNotRunningError:
    location = Path(".")
    robot_log_level = "INFO"


log_name = location / "SeleniumTestability.log"
log_handler = logging.FileHandler(log_name)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log_handler.setFormatter(formatter)
LEVELS = {"FAIL": logging.DEBUG, "WARN": logging.WARN, "INFO": logging.INFO, "DEBUG": logging.DEBUG, "TRACE": logging.DEBUG}


@lru_cache(maxsize=1)
def get_logger(name: str) -> Any:
    lgr = logging.getLogger(name)
    lgr.addHandler(log_handler)
    set_to = LEVELS[robot_log_level]
    lgr.setLevel(set_to)
    lgr.debug(" **** New Session Created for {}  **** ".format(name))
    return lgr


def kwargstr(kwargs: Any) -> str:
    return ", ".join("%s=%r" % x for x in kwargs.items())


def argstr(args: Any) -> str:
    return ", ".join("%s" % x for x in args)

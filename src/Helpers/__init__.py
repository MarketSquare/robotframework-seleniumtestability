# -*- coding: utf-8 -*-
from psutil import Process, wait_procs, NoSuchProcess
from robotlibcore import DynamicCore
from robot.api.deco import keyword
from SeleniumTestability.types import ProcessType


class Helpers(DynamicCore):
    def __init__(self) -> None:
        DynamicCore.__init__(self, [])

    @keyword
    def die_die_die(self, parent: ProcessType) -> None:
        if isinstance(parent, int):
            try:
                par = Process(parent)
            except NoSuchProcess:
                self.warn("Unable to kill process id:{}".format(parent))
                return
        else:
            par = parent
        for child_process in par.children():
            self.die_die_die(child_process)
            if child_process.is_running():
                child_process.terminate()
                _, alive = wait_procs([child_process], timeout=3)
                for p in alive:
                    p.kill()

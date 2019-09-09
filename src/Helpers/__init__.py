# -*- coding: utf-8 -*-
from psutil import Process, wait_procs
from typing import Union
from robotlibcore import DynamicCore, keyword

ProcessType = Union[Process, int]


class Helpers(DynamicCore):

    def __init__(self: "Helpers") -> None:
        DynamicCore.__init__(self, [])

    @keyword
    def die_die_die(self: "Helpers", parent: ProcessType) -> None:
        par = parent
        if isinstance(parent, int):
            par = Process(parent)
        for child_process in par.children():
            self.die_die_die(child_process)
            if child_process.is_running():
                child_process.terminate()
                _, alive = wait_procs([child_process], timeout=3)
                for p in alive:
                    p.kill()

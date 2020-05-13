# -*- coding: utf-8 -*-
from .utils import log_wrapper
from .javascript import JS_LOOKUP
from SeleniumLibrary.base import keyword
from .types import (
    StringArray,
    StorageType,
)
import re
import json


class SeleniumTestability:
    pass


class StorageMixin:
    @log_wrapper
    @keyword
    def get_storage_length(self: "SeleniumTestability", storage_type: str = "localStorage") -> int:
        return self.ctx.driver.execute_script(JS_LOOKUP["storage_length"], storage_type)

    @log_wrapper
    @keyword
    def get_storage_keys(self: "SeleniumTestability", storage_type: str = "localStorage") -> StringArray:
        return self.ctx.driver.execute_script(JS_LOOKUP["storage_keys"], storage_type)

    @log_wrapper
    @keyword
    def get_storage_item(self: "SeleniumTestability", key: str, storage_type: str = "localStorage") -> StorageType:
        matcher = r"^{.*}$"
        storage_item = self.ctx.driver.execute_script(JS_LOOKUP["storage_getitem"], storage_type, key)
        print(f"TYPE OF {key} is {type(storage_item)}")
        if isinstance(storage_item, str) and re.match(matcher, storage_item):
            storage_item = json.loads(storage_item)
        return storage_item

    @log_wrapper
    @keyword
    def set_storage_item(self: "SeleniumTestability", key: str, value: StorageType, storage_type: str = "localStorage") -> None:
        if isinstance(value, dict):
            value = json.dumps(value)
        self.ctx.driver.execute_script(JS_LOOKUP["storage_setitem"], storage_type, key, value)

    @log_wrapper
    @keyword
    def clear_storage(self: "SeleniumTestability", storage_type: str = "localStorage") -> None:
        self.ctx.driver.execute_script(JS_LOOKUP["storage_clear"], storage_type)

    @log_wrapper
    @keyword
    def remove_storage_item(self: "SeleniumTestability", key: str, storage_type: str = "localStorage") -> None:
        return self.ctx.driver.execute_script(JS_LOOKUP["storage_removeitem"], storage_type, key)

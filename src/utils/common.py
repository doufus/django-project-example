# encoding: utf-8
# @Time    : 2021-04-14 15:05
from typing import Any, AnyStr


def getattr_(obj: Any, name: AnyStr, default: Any = '') -> Any:
    if obj is None:
        return ''
    if isinstance(name, list):
        ret = obj
        for row in name:
            if hasattr(ret, row):
                ret = getattr(ret, row)
                if ret == 'null' or ret is None:
                    return default
            else:
                return default
        return ret
    else:
        if hasattr(obj, name):
            ret = getattr(obj, name)
            if ret:
                return ret
            return default
        return default

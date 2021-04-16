# encoding: utf-8
# @Time    : 2021-04-14 16:01
from typing import Optional
from .models import _


class ResponseException(Exception):
    pass


class ControllerException(Exception):
    pass

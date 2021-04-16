# encoding: utf-8
# @Time    : 2021-04-14 16:21
import json
from typing import Optional, List
from src.lib.models import _


class Code(object):

    def __init__(
            self, code: int, message: str = 'error!', examples: Optional[List[str]] = None):
        self.code = code
        self.message = message
        self.examples = examples

    @property
    def result(self):
        return f'[{self.code}] {self.message}'

    def __repr__(self) -> str:
        return str(self.code)

    def __str__(self) -> str:
        return str(self.code)


class ResultCode(object):
    """
        区间              描述
        200              成功，操作成功接收并处理
        40000 - 41000    未授权, 权限错误
        50001 - 59999    接口错误，接口异常
    """
    Code = Code
    C_200 = Code(200, _('成功'))

    C_40001 = Code(40001, _('未授权'))

    C_500 = Code(500, _('服务器内部错误'))
    C_50001 = Code(50001, _('验证参数错误'))

    @classmethod
    def get_msg(cls, code: int) -> str:
        field = 'C_{}'.format(code)
        if hasattr(cls, field):
            if getattr(cls, field):
                return getattr(cls, field).message
        return ''

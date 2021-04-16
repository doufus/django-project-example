# encoding: utf-8
# @Time    : 2021-04-14 17:09
from typing import List, Tuple, Optional
from src.lib.models import _


class Dictionaries(object):

    def __init__(self, choices: List[Tuple[str, str]], default: Optional[str] = None):
        self.choices = choices
        self.df = default if default is not None else self.choices[0][0]

    def __call__(self, *args, **kwargs):
        return self.choices


class PublicChoices(object):

    """ 命名格式 model_name_field_name """

    book_state: Dictionaries = Dictionaries([
        ('draft',  _('草稿')),
        ('shop',  _('上架')),
        ('stock-out',  _('缺货')),
    ])
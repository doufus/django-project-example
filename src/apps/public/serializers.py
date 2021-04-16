# encoding: utf-8
# @Time    : 2021-04-14 17:38
from src.lib.serializers import BaseSerializers, BaseInterfaceParams, params
from .models import BookModel, AuthorModel, _


class BookSerializers(BaseSerializers):
    class Meta(BaseSerializers.Meta):
        model = BookModel


class BookQueryParams(BaseInterfaceParams):
    name = params.CharField(max_length=1024, label=_('姓名'))


class BookBodyParams(BaseInterfaceParams):
    id = params.IntegerField(label=_('ID'), required=True)


class AuthorSerializers(BaseSerializers):
    class Meta(BaseSerializers.Meta):
        model = AuthorModel

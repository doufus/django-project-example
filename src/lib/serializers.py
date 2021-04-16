# encoding: utf-8
# @Time    : 2021-04-14 15:03
import json
import traceback
from abc import ABC

from typing import Any, Dict, List
from django.db import models
from rest_framework import serializers
from rest_framework.exceptions import ErrorDetail
from rest_framework.settings import api_settings
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import html, model_meta, representation
from src.utils import getattr_


class BaseSerializers(serializers.ModelSerializer):
    """ ModelSerializer """
    id = serializers.SerializerMethodField()

    class Meta:

        # 排除字段，exclude和fields不能同一时间使用。
        exclude = ('create_time', 'create_uid', 'write_uid', 'write_time', 'active')

        # 全部字段，指定字段
        # fields = '__all__'
        # fields=('id','name')

        # 关系深度控制
        # depth=1

    @classmethod
    def get_id(cls, instance) -> int:
        _id = getattr_(instance, 'id', default='')
        return _id

    @classmethod
    def set_meta(cls, filed: str, value: Any):
        setattr(cls.Meta, filed, value)

    def create(self, validated_data):
        """
        We have a bit of extra checking around this in order to provide
        descriptive messages when something goes wrong, but this method is
        essentially just:

            return ExampleModel.objects.create(**validated_data)

        If there are many to many fields present on the instance then they
        cannot be set until the model is instantiated, in which case the
        implementation is like so:

            example_relationship = validated_data.pop('example_relationship')
            instance = ExampleModel.objects.create(**validated_data)
            instance.example_relationship = example_relationship
            return instance

        The default implementation also does not handle nested relationships.
        If you want to support writable nested relationships you'll need
        to write an explicit `.create()` method.
        """
        raise_errors_on_nested_writes('create', self, validated_data)

        ModelClass = self.Meta.model

        # Remove many-to-many relationships from validated_data.
        # They are not valid arguments to the default `.create()` method,
        # as they require that the instance has already been saved.
        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        try:
            instance = ModelClass._default_manager.create(**validated_data)
        except TypeError:
            tb = traceback.format_exc()
            msg = (
                    'Got a `TypeError` when calling `%s.%s.create()`. '
                    'This may be because you have a writable field on the '
                    'serializer class that is not a valid argument to '
                    '`%s.%s.create()`. You may need to make the field '
                    'read-only, or override the %s.create() method to handle '
                    'this correctly.\nOriginal exception was:\n %s' %
                    (
                        ModelClass.__name__,
                        ModelClass._default_manager.name,
                        ModelClass.__name__,
                        ModelClass._default_manager.name,
                        self.__class__.__name__,
                        tb
                    )
            )
            raise TypeError(msg)

        # Save many-to-many relationships after the instance is created.
        if many_to_many:
            for field_name, value in many_to_many.items():
                field = getattr(instance, field_name)
                field.set(value)

        return instance


def factory_generate_serializers(model_class: models.Model, meta_fields: str = '__all__',) -> Any:
    """ 动态生成Serializers class """
    class TmpSerializers(BaseSerializers, ABC):

        class Meta:
            model = model_class
            fields = meta_fields

        def get_meta(self):
            return self.Meta
    return TmpSerializers


class BaseInterfaceParams(serializers.Serializer):
    """ 接口参数说明以及验证类 """

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    class Meta:
        pass

    @classmethod
    def set_meta(cls, filed, value):
        setattr(cls.Meta, filed, value)

    @property
    def errors(self):
        ret = super().errors
        # print('###', self.get_fields())
        if isinstance(ret, list) and len(ret) == 1 and getattr(ret[0], 'code', None) == 'null':
            # Edge case. Provide a more descriptive error than
            # "this field may not be null", when no data is passed.
            detail = ErrorDetail('No data provided', code='null')
            ret = {api_settings.NON_FIELD_ERRORS_KEY: [detail]}
        fields = self.get_fields()
        for k, v in ret.items():
            field = fields.get(k)
            if field:
                label = getattr(field, 'label')
                new_v = []
                for r in v:
                    new_v.append(ErrorDetail('{}: {}'.format(label, str(r)), code=r.code))
                ret[k] = new_v
        return ReturnDict(ret, serializer=self)


params = serializers

# encoding: utf-8
# @Time    : 2021-04-14 15:12
import json
from django.forms.utils import pretty_name

from rest_framework import viewsets
from rest_framework.decorators import MethodMapper
from src.lib import mixins

from src.lib.permission import BaseIsAuthenticated, CustomBasePermission
from src.lib.response import BaseResponse
from src.lib.serializers import BaseSerializers
from src.lib.swagger import swagger_auto_schema


def action(methods=None, detail=None, url_path=None, url_name=None, **kwargs):
    """
    Mark a ViewSet method as a routable action.
    Set the `detail` boolean to determine if this action should apply to
    instance/detail requests or collection/list requests.
    """
    methods = ['get'] if (methods is None) else methods
    methods = [method.lower() for method in methods]
    assert detail is not None, (
        "@action() missing required argument: 'detail'"
    )
    # permission_classes
    if kwargs.get('permission_classes'):
        kwargs['permission_classes'].extend([BaseIsAuthenticated, CustomBasePermission])
    else:
        kwargs['permission_classes'] = [BaseIsAuthenticated, CustomBasePermission]
    # name and suffix are mutually exclusive
    if 'name' in kwargs and 'suffix' in kwargs:
        raise TypeError("`name` and `suffix` are mutually exclusive arguments.")

    def decorator(func):
        func.mapping = MethodMapper(func, methods)
        func.detail = detail
        func.url_path = url_path if url_path else func.__name__
        func.url_name = url_name if url_name else func.__name__.replace('_', '-')
        func.kwargs = kwargs
        # Set descriptive arguments for viewsets
        if 'name' not in kwargs and 'suffix' not in kwargs:
            func.kwargs['name'] = pretty_name(func.__name__)
        func.kwargs['description'] = func.__doc__ or None
        return func

    return decorator


class ApiViewSets(viewsets.ViewSet):
    permission_classes = [CustomBasePermission, ]


class BaseModelViewSets(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):

    permission_classes = [CustomBasePermission, ]
    serializer_class = None
    resp = BaseResponse
    json = json
    pk = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_serializer_class(self) -> BaseSerializers:
        serializer = super().get_serializer_class()
        # depth = 1
        # serializer.set_meta('depth', 1)
        return serializer

    def get_object(self):
        obj = super().get_object()
        return obj

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    @swagger_auto_schema()
    def retrieve(self, request, *args, **kwargs):
        """ read """
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema()
    def create(self, request, *args, **kwargs):
        """ create """
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema()
    def destroy(self, request, *args, **kwargs):
        """ delete """
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema()
    def update(self, request, *args, **kwargs):
        """ update """
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema()
    def list(self, request, *args, **kwargs):
        """ list """
        setattr(self.request, 'viewsets', self)
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(self.get_serializer_data(serializer.data))
        serializer = self.get_serializer(queryset, many=True)

        return self.success_response(data=self.get_serializer_data(serializer.data))

    @classmethod
    def get_serializer_data(cls, data):
        return data

    @staticmethod
    def error_response(msg=None, data=None) -> BaseResponse.json:
        return BaseResponse.error(msg, data)

    @staticmethod
    def success_response(msg=None, data=None) -> BaseResponse.json:
        return BaseResponse.success(msg, data)

    @classmethod
    def get_model_class(cls):
        if cls.queryset:
            return cls.queryset.model
        else:
            if cls.serializer_class:
                return cls.serializer_class.Meta.model
        return None

    @classmethod
    def get_resource(cls) -> str:
        model = cls.get_model_class()
        if model:
            if hasattr(model, '_resource'):
                if getattr(model, '_resource'):
                    return getattr(model, '_resource')()
        return ''


__all__ = [
    'BaseModelViewSets', 'ApiViewSets',
    'action'
]

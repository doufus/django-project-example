# encoding: utf-8
# @Time    : 2021-04-14 15:48
from typing import Optional, Any, Dict, List, Type
from drf_yasg.utils import swagger_auto_schema as sa
from drf_yasg.utils import unset
from drf_yasg.openapi import Parameter
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.inspectors import FieldInspector, PaginatorInspector

from src.dictionary import Code
from src.lib.serializers import BaseInterfaceParams
from src.lib.response import ResponseDocs


def swagger_auto_schema(
        method: Optional[str] = None,
        methods: Optional[List[str]] = None,
        auto_schema: Optional[SwaggerAutoSchema] = unset,
        request_body: Optional[Type[BaseInterfaceParams]] = None,
        query_serializer: Optional[Type[BaseInterfaceParams]] = None,
        manual_parameters: Optional[List[Parameter]] = None,
        operation_id: Optional[str] = None,
        operation_description: Optional[str] = None,
        operation_summary: Optional[str] = None,
        security: Optional[List[Dict]] = None,
        deprecated: Optional[bool] = None,
        response_sample: Optional[Dict[Code, Any]] = None,
        response_codes: Optional[List[Code]] = None,
        field_inspectors: Optional[List[Type[FieldInspector]]] = None,
        filter_inspectors: Optional[List[Type[FieldInspector]]] = None,
        paginator_inspectors: Optional[List[Type[PaginatorInspector]]] = None,
        tags: Optional[List[str]] = None,
        **extra_overrides
) -> sa:
    """
        ViewSets类依赖 此装饰器生成文档。
        在 drf_yasg.utils.swagger_auto_schema 之上自定义，详细的参数说明请看此函数

        1. 常用参数说明
            query_serializer: 请求GET的参数, 如果你定义了 BaseInterfaceParams,
            request_body: 请求POST, PUT的参数, 如果你定义了 BaseInterfaceParams,
            operation_summary: 接口标题,
            operation_description: 接口详细说明
            tags: 接口分组, 在文档UI页面分层导航栏显示
            response_sample: 响应示例
            response_codes: 返回错误码列表

        2、 用法：
        class MyViewSets(ViewSets):

            queryset = Model.objects.all()
            serializer_class = Serializers

            # 生成 List ，根據Serializers生成接口
            @swagger_auto_schema()
            def create(self, request, *args, **kwargs):
                return super().create(request, *args, **kwargs)

            # 定义额外接口
            @swagger_auto_schema(
                operation_summary=_('下架'),
                operation_description="# POST /books/stock-out/",
                request_body=BookBodyParams,
                response_codes=[respCode.C_50001, respCode.C_40001]
            )
            @action(detail=False, methods=['post'], url_path='stock-out')  # 定义动作路径
            @controller(controller_class=BookStockOutController, serializer_class=BookBodyParams)  # 业务处理层
            def stock_out(self, request, *args, **kwargs):
                pass

    """

    responses = ResponseDocs(**{'success_response': response_sample, 'error_response': response_codes}).get_responses()
    if operation_description:
        operation_description = '## ' + operation_description.replace('#', '')

    return sa(
        method, methods, auto_schema, request_body,
        query_serializer, manual_parameters, operation_id,
        operation_description, operation_summary, security,
        deprecated, responses, field_inspectors, filter_inspectors,
        paginator_inspectors, tags, **extra_overrides
    )


__all__ = [
    'swagger_auto_schema'
]
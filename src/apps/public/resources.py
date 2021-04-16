# encoding: utf-8
# @Time    : 2021-04-14 17:38
from src.lib.viewsets import BaseModelViewSets, ApiViewSets
from src.lib import swagger_auto_schema, action, controller
from src.lib.controller import Controller
from src.dictionary import ResultCode as respCode
from .models import BookModel, AuthorModel, _
from .serializers import BookSerializers, AuthorSerializers, BookQueryParams, BookBodyParams


class TestViewSet(ApiViewSets):
    @swagger_auto_schema(
        operation_summary=_('测试'),
        operation_description="POST /test/test/",
        request_body=BookBodyParams,
        tags=['测试']
    )
    @action(detail=False, methods=['post'], url_path='test')
    def test(self, request, *args, **kwargs):
        pass


class BookStockOutController(Controller):

    def call(self, *args, **kwargs):
        return self.resp.success()


class BooksViewSet(BaseModelViewSets):
    queryset = BookModel.objects.all()
    serializer_class = BookSerializers

    @swagger_auto_schema(query_serializer=BookQueryParams)
    def list(self, request, *args, **kwargs):
        return super(BooksViewSet, self).list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary=_('下架'),
        operation_description="POST /books/stock-out/",
        request_body=BookBodyParams,
        response_codes=[respCode.C_50001, respCode.C_40001]
    )
    @action(detail=False, methods=['post'], url_path='stock-out')
    @controller(controller_class=BookStockOutController, serializer_class=BookBodyParams)
    def stock_out(self, request, *args, **kwargs):
        pass


class AuthorViewSet(BaseModelViewSets):
    queryset = AuthorModel.objects.all()
    serializer_class = AuthorSerializers

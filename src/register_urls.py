# encoding: utf-8
# @Time    : 2021-04-14 17:34
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from src.lib.generators import CustomOpenAPISchemaGenerator
from src.apps.public.resources import BooksViewSet, AuthorViewSet, TestViewSet
""" 设置接口文档参数
"""
schema_view = get_schema_view(
    openapi.Info(
        title=" API 接口文档平台",    # 必传
        default_version='v1',   # 必传
    ),
    public=True,
    # permission_classes=(permissions.AllowAny,),   # 权限类
    generator_class=CustomOpenAPISchemaGenerator,
)

router = routers.DefaultRouter()
register_urls: [tuple] = [
    (None, BooksViewSet),
    (None, AuthorViewSet),
    ('test', TestViewSet),
]


for url in register_urls:
    path, view_set = url
    try:
        if path is None:
            path = view_set.get_resource()
        router.register(path, view_set, basename=path)
    except Exception as e:
        print(e)

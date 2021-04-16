# encoding: utf-8
# @Time    : 2021-04-16 11:37
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg import openapi


class CustomOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    
    def __init__(self, info=None, version='', url=None, patterns=None, urlconf=None):
        super(CustomOpenAPISchemaGenerator, self).__init__(info, version, url, patterns, urlconf)
    
    def get_schema(self, request=None, public=False):
        """Generate a :class:`.Swagger` object with custom tags"""
        endpoints = self.get_endpoints(request)
        model_resource = {}
        for k, v in endpoints.items():
            try:
                view_set = v[0]
                if hasattr(view_set, 'get_resource') and hasattr(view_set, 'get_model_class'):
                    model = view_set.get_model_class()
                    if hasattr(model, 'get_meta') and hasattr(model.get_meta(), 'verbose_name'):
                        model_resource.update({view_set.get_resource(): model.get_meta().verbose_name})
            except IndexError:
                pass

        swagger = super().get_schema(request, public)
        for k, v in swagger.paths.items():
            for r, u in v.items():
                if isinstance(u, dict):
                    if '_' in u.get('operationId'):
                        operation = u.get('operationId', '').split('_')[1].capitalize()
                        swagger.paths[k][r]['operationId'] = operation
                    for j, tag in enumerate(u.get('tags', [])):
                        if model_resource.get(tag):
                            swagger.paths[k][r]['tags'][j] = model_resource.get(tag)
        return swagger

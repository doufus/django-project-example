# encoding: utf-8
# @Time    : 2021-04-14 15:13
import collections
from typing import Optional, Dict, List, Any
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse, FileResponse
from rest_framework import status
from drf_yasg import openapi

from src.dictionary import ResultCode as respCode
from src.dictionary import Code


class BaseResponse(object):
    """ Response """
    status = status
    response: bool = True
    response_code: int = 0

    @classmethod
    def json(
            cls,
            msg: Optional[str] = None,
            data: Optional[Dict] = None,
            response_status: int = respCode.C_200.code,
            **kwargs
    ) -> JsonResponse:

        assert isinstance(response_status, int)

        result = {'status': response_status, 'msg': msg, 'data': data,
                  'kwargs': kwargs}
        return JsonResponse(result, json_dumps_params={'ensure_ascii': False})

    @classmethod
    def file_response(
            cls,
            file_full_path: str,
            file_name: str,
            file_format: str
    ) -> FileResponse:
        file = open(file_full_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{}.{}"'.format(
            file_name.encode('utf8').decode('ISO-8859-1'), file_format)
        return response

    @classmethod
    def error(
            cls,
            msg: Optional[str] = None,
            data: Optional[dict] = None,
            code: Optional[Code] = None,
    ) -> JsonResponse:

        if code is not None:
            status_ = code.code
            if msg is not None:
                code_msg = '[{}][{}] '.format(code.code, code.message)
                msg = code_msg + msg
        else:
            status_ = respCode.C_500.code
        return cls.json(
            msg or 'Error!', data or {}, response_status=status_
        )

    @classmethod
    def success(
            cls,
            msg: Optional[str] = None,
            data: Optional[dict] = None
    ) -> JsonResponse:
        return cls.json(msg or 'Success!', data or {})


class ResponseDocs(object):

    def __init__(
            self, success_response: Dict[Code, Any] = None,
            error_response: List[Code] = None,
    ):
        self.success_response = success_response if success_response else {respCode.C_200: {}}
        self.error_response = error_response if error_response else []

    def get_responses(self) -> Dict:
        return self.get_schema_dict()

    def get_schema_dict(self) -> Dict:
        # ok
        items = collections.OrderedDict()
        for code, res in self.success_response.items():
            items.update({code.code: openapi.Response(
                description=self.get_ok_code_to_md(code.code, res))})

        if self.error_response:
            items.update(
                {
                    '500': openapi.Response(description=self.get_error_code_to_md())
                }
            )
        return items

    @classmethod
    def get_ok_code_to_md(cls, code: int, md_dict: dict) -> str:
        return """
        响应示例
        ```
        {}
        ```
        """.format({'status': code, 'msg': 'Success!', 'data': md_dict})

    def get_error_code_to_md(self) -> str:
        """将错误码转成md语法格式
        """
        error_code = _('错误码')
        error_msg = _('错误描述')
        md = ['|%(error_code)s|%(error_msg)s|' % {'error_code': error_code, 'error_msg': error_msg}, '|:-|:-:|']
        for code in self.error_response:
            md.append('|%(k)s|%(v)s|' % {'k': code, 'v': respCode.get_msg(code.code)})
        return '\n'.join(md)


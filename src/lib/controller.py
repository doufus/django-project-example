# encoding: utf-8
# @Time    : 2021-04-15 11:58
import abc
from typing import Optional, Type, Any
from functools import wraps
from rest_framework.request import Request
from src.dictionary import ResultCode as respCode
from .models import _
from .response import BaseResponse
from .viewsets import BaseModelViewSets


class Controller(metaclass=abc.ABCMeta):
    """ 业务层抽象类 """
    resp = BaseResponse

    def __init__(self, *args, **kwargs):
        # args = (view_set_class, request_class)
        self.view_set: BaseModelViewSets = args[0]
        self.request: Request = args[1]

        self.args = args
        self.kwargs = kwargs
        self.data = {}
        if hasattr(self.request, 'data'):
            self.data = self.request.data.copy() or {}
        self.filtration_data()

    def filtration_data(self):
        if self.data:
            for k, v in self.data.items():
                if isinstance(v, str):
                    self.data[k] = self.data.get(k).strip()

    @abc.abstractmethod
    def call(self, *args, **kwargs):
        return self.resp.success()

    def __call__(self, *args, **kwargs):
        return self.call()


def controller(
        controller_class: Optional[Any] = None,
        serializer_class: Optional[Any] = None,
):
    """业务控制层
        1. serializer_class 参数验证类,
        2. controller_class 业务执行类,
    """
    def controller_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):

            # 验证
            request = args[1]
            if serializer_class is not None:
                if type(serializer_class).__name__ != 'SerializerMetaclass':
                    BaseResponse.error(
                        code=respCode.C_500, msg=_('必须是rest_framework.serializers.SerializerMetaclass对象')
                    )
                serializer = serializer_class(data=request.data)
                if not serializer.is_valid():
                    return BaseResponse.json(
                        msg=serializer.errors, response_status=respCode.C_50001.code)

            # 执行业务
            if controller_class:
                resp = controller_class(*args, **kwargs)()
                # print('###', controller_class, resp)
                if type(resp).__name__ not in [
                    'JsonResponse', 'HttpResponse', 'StreamingHttpResponse', 'HttpResponseRedirect',
                    'HttpResponsePermanentRedirect', 'HttpResponseGone', 'FileResponse',
                ]:
                    return BaseResponse.error(
                        code=respCode.C_500,
                        msg=_('必须实现call()方法,而且return必须是Response对象。')
                    )
                return resp

            return func(*args, **kwargs)

        return wrapped_function
    return controller_decorator

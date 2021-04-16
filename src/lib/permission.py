# encoding: utf-8
# @Time    : 2021-04-14 15:41
from typing import Optional
from functools import wraps
from abc import ABCMeta, abstractmethod
from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny, BasePermission
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from rest_framework.authentication import TokenAuthentication, get_authorization_header


class BaseSessionAuthentication(SessionAuthentication):
    """使用Django的会话框架进行身份验证。
    """
    pass


class BaseBasicAuthentication(BasicAuthentication):
    """基于用户名/密码的HTTP基本身份验证。
    """
    pass


class BaseIsAuthenticated(IsAuthenticated):
    """只允许经过身份验证的用户访问。
    """
    pass


class BaseIsAdminUser(IsAdminUser):
    """只允许管理用户访问。
    """
    pass


class BaseIsAuthenticatedOrReadOnly(IsAuthenticatedOrReadOnly):
    """请求被认证为用户，只读。
    """
    pass


class BaseAllowAny(AllowAny):
    """允许任何访问。
    """
    pass


class BaseTokenAuthentication(TokenAuthentication):

    get_keyword = 'Token'
    callback_token = ''

    def authenticate(self, request):
        """更改token验证方式， 允许token存在于GET参数中以及请求头中
        """
        auth = get_authorization_header(request).split()
        token = request.GET.get(self.get_keyword)
        if token and len(auth) < 1:
            auth = [self.get_keyword.encode(), token.encode()]
        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        if self.callback_token and token in self.callback_token and '/api/cb/' not in request.path:
            msg = _('此token只能用于回调.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)


class CustomBasePermission(BasePermission):
    """自定义权限类
       判断用户是否拥有权限
    """
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        # print('---------------------------', request, view.get_view_name(), view.get_throttles())
        return True

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        # print('=======================')
        return True

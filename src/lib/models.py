# encoding: utf-8
# @Time    : 2021-04-14 14:57
import abc
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseManager(models.Manager):
    """ 模型管理类 """
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(active=1)


class BaseModel(models.Model):
    """ 模型基类 """

    create_time = models.DateTimeField(auto_now_add=True, verbose_name=_('创建时间'))
    create_uid = models.IntegerField(default=0, blank=True, verbose_name=_('创建用户'))
    write_uid = models.IntegerField(default=0, blank=True, verbose_name=_('修改用户'))
    write_time = models.DateTimeField(auto_now=True, verbose_name=_('创建时间'))
    active = models.BooleanField(verbose_name=_('是否删除?'), default=True)

    objects = BaseManager()

    class Meta:
        abstract = True
        ordering = ['-id']

    @classmethod
    def get_meta(cls) -> Meta:
        return cls._meta

    @staticmethod
    @abc.abstractmethod
    def _resource():
        return ''

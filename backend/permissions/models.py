import binascii
import os
from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _


class Routes1(models.Model):
    """
    1级路由
    """
    path = models.CharField(max_length=128, unique=True, verbose_name='path')
    component = models.CharField(max_length=128, verbose_name='组件', default='layout/Layout', blank=True)
    redirect = models.CharField(max_length=128, verbose_name='重定向地址', blank=True)  # 重定向地址，在面包屑中点击会重定向去的地址
    name = models.CharField(max_length=128, unique=True, verbose_name='路由名称', blank=True)
    title = models.CharField(max_length=128, verbose_name='标题', blank=True)
    icon = models.CharField(max_length=128, verbose_name='图标', blank=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name=_("角色"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all url "
            "granted to each of their groups."
        )
    )

    class Meta:
        db_table = 'routes1'


class Routes2(models.Model):
    """
    2级路由
    """
    path = models.CharField(max_length=128, unique=True, verbose_name='path')
    component = models.CharField(max_length=128, verbose_name='组件')
    name = models.CharField(max_length=128, unique=True, verbose_name='路由名称')
    title = models.CharField(max_length=128, verbose_name='标题')
    routes1 = models.ForeignKey('Routes1', on_delete=models.CASCADE)

    class Meta:
        db_table = 'routes2'


class ApiPermission(models.Model):
    """
    接口权限
    """
    name = models.CharField(max_length=128, unique=True, verbose_name='接口名称')
    url = models.CharField(max_length=128, unique=True, verbose_name='url')
    method = models.CharField(max_length=128, verbose_name='请求方式')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    groups = models.ManyToManyField(
        Group,
        verbose_name=_("角色"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all url "
            "granted to each of their groups."
        )
    )

    class Meta:
        db_table = 'api_permission'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=128, blank=True, null=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        db_table = 'profile'

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()
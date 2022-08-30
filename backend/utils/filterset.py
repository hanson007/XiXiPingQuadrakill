"""
django-filter 过滤器
"""
import django_filters
from django.contrib.auth.models import User, Group
from permissions.models import Profile, Routes1, Routes2


class UserFilter(django_filters.rest_framework.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = User
        fields = ['username', 'email']


class GroupFilter(django_filters.rest_framework.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Group
        fields = ['name']


class Routes1Filter(django_filters.rest_framework.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    path = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Routes1
        fields = ['name', 'path']


class Routes2Filter(django_filters.rest_framework.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    path = django_filters.CharFilter(lookup_expr='icontains')
    routes1 = django_filters.CharFilter()
    class Meta:
        model = Routes2
        fields = ['name', 'path', 'routes1']
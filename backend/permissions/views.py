import datetime
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.models import User, Group
from utils import status as my_status
from utils import login_auth
from utils import filterset
from permissions.models import Profile, Routes1, Routes2
from permissions.serializers import (UserSerializer, GroupSerializer, TokenSerializer,
                                     Routes1Serializer, Routes2Serializer)
from django.http import Http404
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth import authenticate, login
from django_filters.rest_framework import DjangoFilterBackend


class UserViewSet(viewsets.ModelViewSet):
    """
    允许用户查看或编辑的API路径。
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filterset.UserFilter


class GroupViewSet(viewsets.ModelViewSet):
    """
    允许组查看或编辑的API路径。
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filterset.GroupFilter


class Routes1ViewSet(viewsets.ModelViewSet):
    """
    1级路由
    """
    queryset = Routes1.objects.all()
    serializer_class = Routes1Serializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filterset.Routes1Filter


class Routes2ViewSet(viewsets.ModelViewSet):
    """
    2级路由。
    """
    queryset = Routes2.objects.all()
    serializer_class = Routes2Serializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filterset.Routes2Filter


class Login(APIView):
    """
    登录
    """
    permission_classes = ()

    def _get_or_create(self, user):
        if Profile.objects.filter(user=user).exists():
            profile = Profile.objects.get(user=user)
            days = (datetime.datetime.now(datetime.timezone.utc) - profile.create_time).days
            # 如果token过期7天需要重新生成
            if days > settings.USER_TOKEN_COOKIE_EXPIRATION_DAYS:
                profile.token = Profile.generate_key()
                profile.save()
        else:
            profile = Profile.objects.create(user=user, token=Profile.generate_key())
        return profile

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # login(request, user)
            profile = self._get_or_create(user)
            data = {
                'code': my_status.SUCCESS_20000,
                'content': profile.token,
                'message': ''
            }
        else:
            data = {
                'code': my_status.Authentication_Failed_40021,
                'content': '',
                'message': serializer.errors
            }
        return Response(data)


class GetLoginUser(APIView):
    """获取登录用户"""
    authentication_classes = (login_auth.Authentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        print(request.user)
        data = {
            'code': my_status.SUCCESS_20000,
            'content': UserSerializer(request.user, context={'request': request}).data,
            'message': ''
        }
        return Response(data)


class AsyncRoutes(APIView):
    """
    动态生成路由
        根据用户的角色动态生成路由
    """
    authentication_classes = (login_auth.Authentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        groups = request.user.groups.all()
        routes = []
        for g in groups:
            routes1 = Routes1.objects.filter(groups=g)
            for r1 in routes1:
                routes2 = Routes2.objects.filter(routes1=r1).values()
                r1_values = Routes1Serializer(r1).data
                r1_values['children'] = list(routes2)
                routes.append(r1_values)
        import pprint
        pprint.pprint(routes)
        data = {
            'code': my_status.SUCCESS_20000,
            'content': routes,
            'message': ''
        }
        return Response(data)

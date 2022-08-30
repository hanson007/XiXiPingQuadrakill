"""
登录认证
"""
import datetime
from django.conf import settings
from permissions.models import Profile
from rest_framework import authentication
from rest_framework import exceptions


class Authentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get(settings.USER_TOKEN_COOKIE_NAME)
        if not token:
            raise exceptions.NotAuthenticated('请登录认证！')

        if Profile.objects.filter(token=token).exists():
            profile = Profile.objects.get(token=token)
            days = (datetime.datetime.now(datetime.timezone.utc) - profile.create_time).days
            # 如果token过期7天需要重新生成
            if days > settings.USER_TOKEN_COOKIE_EXPIRATION_DAYS:
                raise exceptions.AuthenticationFailed('token过期，请重新登录')
        else:
            raise exceptions.AuthenticationFailed('没有这个用户')

        return (profile.user, None)
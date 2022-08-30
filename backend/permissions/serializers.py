#!/usr/bin/python env
# -*- coding: UTF-8 -*-
# Description:                    
# Author:           hanson
# Date:             2022年08月17日
# Company:          League of Legends
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from permissions.models import Profile, Routes1, Routes2


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    # groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups', 'id')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile



class Routes1Serializer(serializers.ModelSerializer):
    from rest_framework.validators import UniqueValidator

    path = serializers.CharField(
        max_length=128,
        validators=[UniqueValidator(queryset=Routes1.objects.all(), message='路径已存在')],
        error_messages={'blank': _('路径不能为空'), }
    )
    class Meta:
        model = Routes1
        fields = '__all__'


class Routes2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Routes2
        fields = '__all__'


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128)
    password = serializers.CharField(max_length=128)
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('用户名或密码错误')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

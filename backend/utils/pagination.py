#!/usr/bin/python env
# -*- coding: UTF-8 -*-
# Description:      分页
# Author:           hanson
# Date:             2022年08月26日
# Company:          League of Legends
# 在 pagination.py 文件里写一个通用的分页器
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from utils import status as my_status
from collections import OrderedDict


class CPageNumberPagination(PageNumberPagination):
    page_size = None  # 默认每页显示条数配置, None 不启用分页
    page_size_query_param = "page_size"  # “分页大小”的请求参数名称
    page_query_param = "page"  # “页数”的请求参数名称, 默认是page
    max_page_size = 1000  # 最大显示条数

    # 觉得不适用, 那就拷贝出来,重载函数, 自己多加几个字段.
    # (可通过官方文档或直接调试得知从哪些属性获取正确的值.)
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('code', my_status.SUCCESS_20000),
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('page', self.page.number),
            ('total_page', self.page.paginator.num_pages),
            ('page_size', self.page.paginator.per_page),
            ('results', data)
        ]))

'''
自定义返回处理
'''

# 导入控制返回的JSON格式的类
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from utils import status as my_status


class CustomJSONRenderer(JSONRenderer):
    # 重构render方法
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context:
            # 响应的信息，成功和错误的都是这个
            # 成功和异常响应的信息，异常信息在前面自定义异常处理中已经处理为{'message': 'error'}这种格式
            # print(data)
            if renderer_context["response"].status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]:
                default_code = my_status.SUCCESS_20000
            else:
                default_code = renderer_context["response"].status_code

            # 如果返回的data为字典
            if isinstance(data, dict):
                # 响应信息中有message和code这两个key，则获取响应信息中的message和code，并且将原本data中的这两个key删除，放在自定义响应信息里
                # 响应信息中没有则将msg内容改为请求成功 code改为请求的状态码
                message = data.pop('message', '请求成功')
                code = data.pop('code', default_code)
            # 如果不是字典则将msg内容改为请求成功 code改为请求的状态码
            else:
                message = '请求成功'
                code = default_code
            # 自定义返回的格式
            ret = {
                'message': message,
                'code': code,
                'data': data,
            }
            # 返回JSON数据
            return super().render(ret, accepted_media_type, renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)

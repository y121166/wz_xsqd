# 登录验证
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse


def auth(func):
    """
    判断是否登录装饰器
    :param func:
    :return:
    """
    # todo
    # 待完善ajax请求的session状态验证
    def inner(request, *args, **kwargs):
        response_data = {}
        ck = request.session.get('user_id', 'None')
        is_ajax = request.is_ajax()
        # print("-------%s" % is_ajax)
        if is_ajax and ck == 'None':
            response_data['result'] = 'timeout'
            response_data['message'] = '登录超时，请重新登录！'
            return JsonResponse(response_data, safe=False)
        elif ck == 'None':
            return redirect(settings.LOGIN_URL)
        return func(request, *args, **kwargs)
    return inner

# 登录验证
from django.conf import settings
from django.shortcuts import redirect


def auth(func):
    """
    判断是否登录装饰器
    :param func:
    :return:
    """
    # todo
    # 待完善ajax请求的session状态验证
    def inner(request, *args, **kwargs):
        ck = request.session.get('user_id', 'None')
        if ck == 'None':
            return redirect(settings.LOGIN_URL)
        return func(request, *args, **kwargs)
    return inner

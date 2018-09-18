# 登录验证
from django.conf import settings
from django.shortcuts import redirect


def auth(func):
    """
    判断是否登录装饰器
    :param func:
    :return:
    """
    def inner(request, *args, **kwargs):
        ck = request.session.get('user_id')
        print(ck)
        if ck == 'none':
            return redirect(settings.LOGIN_URL)
        return func(request, *args, **kwargs)
    return inner

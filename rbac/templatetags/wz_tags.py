# -*- coding:utf-8 -*-
# @Time    :2018-11-06 15:28
# @Author  :于厚良
# @Email   :yu_houliang@163.com
# @File    :wz_tags.py
# @Software:PyCharm
from django import template
from django.utils.safestring import mark_safe

register = template.Library()  # register的名字是固定的,不可改变


######################自定义标签####################

@register.simple_tag
def simple_tag_detailZyh(v1, v2, v3):
    print(v1, v2, v3)
    return v1 - v2 - v3

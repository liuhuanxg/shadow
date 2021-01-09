#-*-coding:utf-8 -*-
from django import template

register = template.Library()

@register.filter
def set_password(value):
    return "*"*10
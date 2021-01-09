# -*-coding:utf-8 -*-
"""

"""
from django.shortcuts import HttpResponse
from home.models import KeyWords


def delete_kw(request):
    KeyWords.objects.all().delete()
    return HttpResponse("delete success！")


if __name__ == '__main__':
    delete_kw()

# -*-coding:utf-8 -*-

from django.urls import path, include, re_path
from .views import *
from django.contrib import admin

urlpatterns = [
    re_path('^$', index),
    path('index/', index),
    path('login/', login),
    path('register/', register),
    path('search/', search),
    path('save_url/', save_url),
    path('praise_step/', praise_step),
    path('complaint/', complaint),
]

from home.delete_data import *

urlpatterns += [
    path("delete_kw/", delete_kw)
]

app_name = "home"

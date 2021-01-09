#-*-coding:utf-8 -*-

import hashlib
def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result


from home.models import User
from django.http import HttpResponseRedirect

# 登录校验器
def loginValid(func):
    def inner(request, *args, **kwargs):
        # 从cookie当中获取数据
        username = request.COOKIES.get("username")
        id = request.session.get("user_id")
        # 判断cookie存在
        if username and id:
            # 通过id查询用户
            user = User.objects.filter(id=id).first()
            if user and user.username == username:  # 证明id时这个用户名对应的id
                return func(request, *args, **kwargs)  # 跳转页面
        return HttpResponseRedirect("/login/")
    return inner







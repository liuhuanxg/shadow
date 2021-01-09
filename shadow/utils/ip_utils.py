# -*-coding:utf-8 -*-


def get_user_ip(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:  # 获取用户真实IP地址
        user_ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        user_ip = request.META['REMOTE_ADDR']
    username = request.META['USERNAME']
    print(username, user_ip)
    return user_ip

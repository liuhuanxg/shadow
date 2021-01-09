#-*-coding:utf-8 -*-


# 发送邮件
from django.core.mail import send_mail
from shadow import settings
def send_email(message,receiver,html_message=None):
    """
    :param message: 要发送的信息
    :param receiver: 接收人
    :param html_message: html类型内容
    :return:
    """
    try:
        if html_message:
            result = send_mail("",message,settings.EMAIL_HOST_USER,[receiver],html_message=html_message)
        else:
            result = send_mail("",message,settings.EMAIL_HOST_USER,[receiver])
    except:
        result = 0
    return result
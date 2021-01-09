from django.shortcuts import render, redirect
from utils import (parse_baidu, parse_google, parse_bing, ip_utils, date_utils, pinyin_utils)
from django.http import JsonResponse
from .models import *
import traceback
import datetime
from django.shortcuts import HttpResponseRedirect, HttpResponse
from string import ascii_letters, digits
import random
import json
from django.db.models import Q, F
from django.views.decorators.csrf import csrf_exempt
from math import *
from threading import Thread


def login(request):
    return redirect("https://shadowq.com/member.php?mod=logging&action=login&referer=")


def register(request):
    return redirect("https://shadowq.com/member.php?mod=newregister")


def index(request):
    """
    首页
    :param request:
    :return:
    """
    resp = {}
    return render(request, "index.html")


def search(request):
    """
    :param request:
    :return:
    """
    data = []
    request_data = request.GET
    keywords = request_data.get("kw", "").strip()
    try:
        if keywords:
            kw_lst = KeyWords.objects.filter(word_name__icontains=keywords).values_list("id", flat=True)
            print("kw_lst", kw_lst)
            if not kw_lst.exists():  # 关键词不存在就存储关键词
                kw_obj = KeyWords()
                kw_obj.word_name = keywords
                kw_obj.pinyin = json.dumps(pinyin_utils.set_pinyin(keywords))
                kw_obj.save()
                key_id = kw_obj.id
            else:
                key_id = kw_lst[0]
            count = WordsDetail.objects.filter(key_id=key_id).count()
            if count < 300:
                count = 300 - count
                number = count // 30
                print("数量：", number)
                t1 = Thread(target=parse_baidu.parse_baidu, args=(keywords, number, key_id))
                t2 = Thread(target=parse_bing.parse_bing, args=(keywords, number, key_id))
                # t3 = Thread(target=parse_google.parse_google,args=(keywords,number,key_id))
                t1.start()
                t2.start()
                t1.join()
                t2.join()
                # t3.start()
            data = WordsDetail.objects.filter(key_id=key_id)
    except:
        print("search", traceback.format_exc())
    return render(request, "search_result.html", {"data": data, "keywords": keywords})


def save_url(request):
    """
    :param request:
    :return:
    """
    resp = {"status": 1, "href": ""}
    data = request.GET
    href_id = data.get("href_id", "")
    try:
        detail = WordsDetail.objects.filter(id=href_id).first()
        resp["href"] = detail.href
        user_ip = ip_utils.get_user_ip(request)
        if detail:
            click_count = ClickCount.objects.filter(href_id__href=href_id, date=date_utils.get_now_date()).first()
            if click_count:
                # 如果ip不在当天点击的ip里边
                if user_ip not in json.loads(click_count.ips):
                    click_count.count = F("count") + 1
                    click_count.save()
                    if (F("count") + 1) % detail.data_source.click_number == 0:
                        detail.score = F("score") + 0.0001
                        detail.save()
            else:
                ClickCount.objects.create(href_id=detail.id, ips=json.dumps([user_ip]))
    except:
        print("save_url", traceback.format_exc())
    return JsonResponse(resp)


@csrf_exempt
def praise_step(request):
    """
    点赞或者点踩
    :param request:
    :return:
    """
    response = {"status": 1}
    try:
        href_id = request.POST.get("href_id", "")
        user = request.session.get("user_id", 1)
        action = request.POST.get("action", 0)
        wd = WordsDetail.objects.filter(id=href_id).first()
        if wd:  # 链接已经存在WordsDetail表中
            action_record = ActionRecord.objects.get_or_create(href_id=wd.id, user_id=user, action=action)
            print("action_record", action_record)
            if action_record[1] == True:  # True代表创建
                if action == "1":
                    wd.support_count = F("support_count") + 1
                else:
                    wd.step_count = F("step_count") + 1
                wd.save()
        else:
            response["status"] = 0
    except:
        print("praise_step", traceback.format_exc())
    return JsonResponse(response)


# 投诉
def complaint(request):
    href_id = request.GET.get("id")
    types = ComplaintType.objects.all()
    if request.method == "POST":
        id = request.POST.get("id")
        comment = request.POST.get("comment")
        types = request.POST.getlist("types")  # 举报类型
        user_id = request.session.get("user_id", 1)
        print("types", types, type(types))
        wd = WordsDetail.objects.filter(id=id).first()
        if wd:
            ComplaintRecord.objects.create(href_id=id, user_id=user_id, comment=comment, types=json.dumps(types))
        return HttpResponse("投诉成功")
    return render(request, "comlaint.html", {"id": href_id, "types": types})

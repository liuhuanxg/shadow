# -*-coding:utf-8 -*-

import urllib3
import requests
from lxml import etree
from threading import Thread
from home.models import WordsDetail, EngineScore
import json
from utils.pinyin_utils import set_pinyin
import traceback
import config


def parse_baidu(keyword, number, key_id):
    url = "https://www.baidu.com/s"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    }
    for i in range(number):
        param = {
            "wd": keyword,
            "pn": 0 + i * 10
        }
        response = requests.get(url=url, headers=headers, params=param)
        text = response.text
        tree = etree.HTML(text)
        content_left = tree.xpath('//div[@id="content_left"]/div')
        print(len(content_left))
        engine_name = config.Engine_lst[0]
        engine = EngineScore.get_one(engine_name=engine_name)
        for c in content_left:
            try:
                href = c.xpath('.//h3/a/@href')[0]
                detail_name = c.xpath('.//h3/a')[0].xpath("string(.)").strip()
                src = c.xpath('.//div[1]/div[1]/a/img/@src')
                if src:
                    src = src[0]
                    content_tree = c.xpath('./div[1]/div[2]/div')
                    content = content_tree[0].xpath("string(.)")
                    # print(111, content)
                    gg = content_tree[-1].xpath("string(.)")
                    if "广告" in gg:  # 包含广告就删除
                        # print("广告", gg)
                        continue
                else:
                    src = ""
                    content = c.xpath('.//div')[0].xpath("string(.)")
                    print(2222, content)
                    if "广告" in content:  # 包含广告就删除
                        continue
                content = content.strip().replace("\n", " ")

                result = WordsDetail.objects.get_or_create(href=href, key_id_id=key_id, data_source_id=engine.id)
                if result[1]:
                    word_detail = result[0]
                    word_detail.detail_name = detail_name
                    word_detail.src = src
                    word_detail.content = content
                    word_detail.score = engine.weight  # 设置初始权重
                    word_detail.pinyin = json.dumps(set_pinyin(detail_name))
                    word_detail.save()
            except:
                print(url + "?wd={}&pn={}".format(keyword, 0 + i * 10))
                print(traceback.format_exc())


if __name__ == '__main__':
    keywords = "影子论坛"
    number = 10
    t1 = Thread(target=parse_baidu, args=(keywords, number, 1))
    # print(parse_baidu(keywords, number))
    result = t1.start()
    print(result)

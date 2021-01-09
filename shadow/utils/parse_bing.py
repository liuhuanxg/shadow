# -*- coding: utf-8 -*-
import requests
from lxml import etree
# from home.models import WordsDetail, KeyWords, EngineScore
# import json
# from utils.pinyin_utils import set_pinyin
import config
import traceback


def parse_bing(keyword, number, key_id):
    url = "https://cn.bing.com/search"

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"}
    result = []
    engine_name = config.Engine_lst[1]
    # engine = EngineScore.get_one(engine_name=engine_name)
    for i in range(number):
        params = {"q": keyword, "first": 1 + i * 10}
        resp = requests.get(url=url, headers=headers, params=params)
        if resp.status_code == 200:
            tree = etree.HTML(resp.text)
            # with open("bing.html","wb")as fp:
            #     fp.write(resp.content)
            # data_tree = tree.xpath('/ol[@id="b_results"]/li[@class="b_algo"]')
            data_tree = tree.xpath('//li[@class="b_algo"]')
            # print(data_tree)

            for data in data_tree:
                index = 1
                try:
                    href = data.xpath(".//h2/a/@href")
                    detail_name = data.xpath(".//h2/a")
                    content = data.xpath('./div[@class="b_caption"]')
                    if not href or not detail_name or not content:
                        print(href, detail_name, content)
                        print(url, keyword, 1 + i * 10, index)
                        content = content[0].xpath("string(.)").strip().replace("\n", " ")
                        print(content)
                        continue
                    index += 1
                    href = href[0]
                    detail_name = detail_name[0].xpath("string(.)").strip().replace(" ", "")
                    content = content[0].xpath("string(.)").strip().replace("\n", " ")
                    result.append({
                        "detail_name": detail_name,
                        "content": content,
                        "href": href,
                        "src": ""
                    })
                    # result = WordsDetail.objects.get_or_create(href=href,
                    #                                            key_id_id=key_id,
                    #                                            data_source_id=engine.id)
                    #
                    # if result[1]:
                    #     word_detail = result[0]
                    #     word_detail.detail_name = detail_name
                    #     word_detail.src = ""
                    #     word_detail.content = content
                    #     word_detail.pinyin = json.dumps(set_pinyin(detail_name))
                    #     word_detail.score = engine.weight
                    #     word_detail.save()
                except:
                    print(traceback.format_exc())
    return result


if __name__ == '__main__':
    print(parse_bing("小米", 10, 1))

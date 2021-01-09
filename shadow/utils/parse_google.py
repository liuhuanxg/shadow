# -*-coding:utf-8 -*-
"""
@project:shadow
"""
from requests import get
from lxml import etree
from home.models import WordsDetail, EngineScore
import json
from utils.pinyin_utils import set_pinyin
import config


def parse_google(keywords, key_id, number_results=10, language_code="en"):
    usr_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/61.0.3163.100 Safari/537.36'}
    escaped_search_term = keywords.replace(' ', '+')

    google_url = 'https://www.google.com/search?q={}&num={}&hl={}' \
        .format(escaped_search_term, number_results + 10, language_code)
    response = get(google_url, headers=usr_agent)
    response.raise_for_status()
    return parse_results(response.text, key_id)


def parse_results(raw_html, key_id):
    tree = etree.HTML(raw_html)
    result_block = tree.xpath('//div[@class="rc"]')
    result = []
    engine_name = config.Engine_lst[2]
    engine = EngineScore.get_one(engine_name=engine_name)
    for result in result_block:
        href = result.xpath('.//a/@href')
        detail_name = result.xpath('string(.//h3)')
        content = result.xpath('.//div[@class="IsZvec"]')
        if not href or not detail_name or not content:
            print(href, detail_name, content)
            continue
        href = href[0]
        detail_name = detail_name[0]
        content = content[0].xpath("string(.)").strip().replace("\n", " ")
        result.append({
            "detail_name": detail_name,
            "href": href,
            "src": "",
            "content": content,
        })
        result = WordsDetail.objects.get_or_create(href=href, key_id_id=key_id, data_source_id=engine.id)
        if result[1]:
            word_detail = result[0]
            word_detail.detail_name = detail_name
            word_detail.src = ""
            word_detail.content = content
            word_detail.score = engine.weight  # 设置初始权重
            word_detail.pinyin = json.dumps(set_pinyin(detail_name))
            word_detail.save()
    return result


if __name__ == '__main__':
    parse_google("高效码农", 1)

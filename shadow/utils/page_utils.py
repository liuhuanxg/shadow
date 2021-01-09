#-*-coding:utf-8 -*-
from django.core.paginator import Paginator  #引入分页器
def set_page(data,num,page):
    """
    :param data: 所有的数据
    :param num:  每页的数据
    :param page: 当前的页码
    :return:
    """
    p = Paginator(data,num)
    number = p.num_pages
    page_range = p.page_range
    try:
        page = int(page)
        data = p.page(page)
    except:
        data = p.page(1)
    if page < 5:  # 一次只返回5个页码
        page_list = page_range[:5]
    elif page + 4 > number:
        page_list = page_range[-5:]
    else:
        page_list = page_range[page - 3:page + 2]
    return data,page_list
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/15 14:26
# @Author  : Aries
# @Site    : 
# @File    : spider-ttjiepa.py
# @Software: PyCharm Community Edition
#分析ajax爬取今日头条的街拍图片
import random
import json
import re
import os
import  requests
from multiprocessing import pool
from urllib.parse import urlencode
from urllib.error import URLError
def get_page_index(offset, keyword):
    data = {
        'autoload': 'true',
        'count': 20,
        'cur_tab': 3,
        'format': 'json',
        'keyword': keyword,
        'offset': offset,
        'from':'gallery'
    }
    url = 'http://www.toutiao.com/search_content/?'+ urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code==200:
            # print(response.text)
            return response.text
        else:
            print('页面加载出错')
    except URLError as e:
        print(e.reason)
def parse_page_url(data):
    json_data=json.loads(data)
    for items in json_data.get('data'):
        # print(items.get('article_url'))
        yield items.get('article_url')

def get_page_detail(article_url):
    response=requests.get(article_url)
    # print(response.text)
    pattern=re.compile('.*?gallery: JSON.parse\("(.*)"\).*?', re.S)
    title_pattern=re.compile('<title>(.*?)</title>.*?')
    title=re.search(title_pattern,response.text).group(1)
    results=re.search(pattern,response.text)
    if results:
        data=json.loads(results.group(1).replace('\\',''))
        sub_images=data.get('sub_images')
        for image_url in sub_images:
            url=image_url.get('url')
            save_iamges(url,title)
            print('图片保存成功')

def save_iamges(url,title):
    response=requests.get(url)
    path='e:/downloads/'+title+'/'
    filename = str(random.randint(0, 100)) + '.jpg'
    if not os.path.exists(path):
         os.mkdir(path)
         with open(path+filename,'wb') as f:
            f.write(response.content)
            f.close()
    else:
         with open(path + filename, 'wb') as f:
            f.write(response.content)
            f.close()

if __name__ == '__main__':
    for offset in range(1,10):
        data=get_page_index(offset*20,'街拍')
        article_urls=parse_page_url(data)
        for article_url in article_urls:
            try:
                print('当前正在抓取的页面是'+article_url)
                get_page_detail(article_url)
            except:
                pass
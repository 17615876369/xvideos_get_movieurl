# -*- coding: utf-8 -*-
# @Time    : 2020/10/16 0016 下午 20:06
# @Author  : 王约翰
# @Email   : 296334356@qq.com
# @File    : xvideos_get_url.py

import requests
import re
from bs4 import BeautifulSoup
import time


def get_url(kws, page):
    headers = {

        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
    }
    url = "https://www.xvideos.com/?k=%sp=%s" % (kws, page)

    html = requests.get(url, headers=headers).text
    # with open('01.html', 'r', encoding='utf8')as f:
    #     html = f.read()
    # soup = BeautifulSoup(html, features="lxml")
    # tags = soup.find_all(name='div', attrs={"class": "thumb-block  tbm-init-ok"})
    rule = '<div class="thumb"><a href="(.*?)">'
    tags = re.findall(rule, html)
    urls = []
    for i in tags:
        ur = 'https://www.xvideos.com' + i
        urls.append(ur)
    urls = urls[:27]
    return urls

def get_name(movie_url):
    headers = {

        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
    }
    url = movie_url

    html = requests.get(url, headers=headers).text

    # with open('01.html', 'r', encoding='utf8')as f:
    #     html = f.read()
    # soup = BeautifulSoup(html, features="html.parser")
    # tags = soup.find_all(name='p', attrs={"class": "title"})

    rule = r'<title>(.*?) - XVIDEOS.COM</title>'
    name = re.findall(rule, html)
    return name[0]

def Parsing_video(urls):
    url = 'https://superparse.com/zh'
    for get_url in urls:
        data = {'url': get_url}
        from_data = {"data": data}

        headers = {
                "Referer": "https://superparse.com/zh",  # 必须带这个参数，不然会报错
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
                     }


        html = requests.post(url, data=data, headers=headers).text
        soup = BeautifulSoup(html, features="html.parser")
        tags = (soup.find_all(name='a', attrs={"class": "btn btn-success"}))
        try:
            tag = tags[1]
            movie_url = (tag['href'])
            name = get_name(get_url)
            print(name)
            print(movie_url)
            with open(kws + 'data.log', 'a')as f:
                f.writelines(name + ';' + movie_url + '\n')
        except:
            tag = tags[0]
            movie_url = (tag['href'])
            name = get_name(get_url)
            print(name)
            print(movie_url)
            with open(kws + 'data.log', 'a')as f:
                f.writelines(name + ';' + movie_url + '\n')



if __name__ == '__main__':
    kws = input('请输入想要搜索的关键字:')
    page = input('请输入想要下载的页数:')
    if int(page) > 0:
        page = int(page)
        for i in range(page):
            urls = get_url(kws, i)
            Parsing_video(urls)
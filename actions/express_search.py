#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: Hou-Hou

"""
@File: express_search.py
@Date: 2021-01-23
@Author: houjingjing0203@163.com.com
@Version: 
"""

import requests
import time

express_list = {
    "圆通": "yuantong",
    "顺丰": "shunfeng",
    "中通": "zhongtong"
}


def get_express_response(express, number):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        "Referer": "http://www.kuaidi.com/cominterface2345.html"
    }
    now_time = str(int(time.time() * 1000))
    url = 'http://www.kuaidi.com/index-ajaxselectcourierinfo-' + number + '-' + express + '-UUCAO' + now_time + '.html'
    response = requests.get(url=url, headers=headers)

    return response
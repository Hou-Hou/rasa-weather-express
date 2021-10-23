#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: Hou-Hou

"""
@File: weather_search.py
@Date: 2021-01-25
@Author: houjingjing0203@163.com.com
@Version: 
"""

import numpy as np
import pandas as pd
import requests
from requests import (
    ConnectionError,
    HTTPError,
    TooManyRedirects,
    Timeout
)

# KEY = 'S-WcZsH3gzQ1Vyyu4'
# KEY = 'rmhrne8hal69uwyv'   # 老师
# language = 'zh-Hans'
# 'https://api.seniverse.com/v3/weather/now.json?key=your_api_key&location=beijing&language=zh-Hans&unit=c#%E5%8F%82%E6%95%B0'
API = 'https://api.seniverse.com/v3/weather/daily.json'  # API URL，可替换为其他 URL

def fetch_weather(location, start=0, days=15):
    """
    从天气网站查询天气
    :param location: 地点
    :param start: 从哪天开始，今天：start=0，昨天：start=-1，明天：start=1
    :param days: 从start开始，查询的天数
    :return:
    """
    params = {'key': 'rmhrne8hal69uwyv',
              'location': location,
              'language': 'zh-Hans',
              'unit': 'c',
              'start': start,
              'days': days}

    result = requests.get(API, params=params, timeout=2)

    return result.json()


def get_result(address, date_time, date_time_number):
    """
    处理查询结果为返回user的天气格式
    :param address:
    :param date_time:
    :param date_time_number:  今天 date_time_number=0； 明天 date_time_number=1
    :return:
    """
    try:
        results = fetch_weather(address)
        result = {
            "location": results["results"][0]["location"],
            "result": results["results"][0]["daily"][date_time_number]
        }
        '''
        ["daily"][0]：今天
        '''
    except (ConnectionError, HTTPError, TooManyRedirects, Timeout) as e:
        text_message = "{}".format(e)
    else:
        text_message_tpl = """
        {} {} ({}) 的天气情况为：\n
            白天：{}；夜晚：{}；气温：{}-{} °C；风向：{}，风速：{}
        """
        text_message = text_message_tpl.format(
            result['location']['name'],
            date_time,
            result['result']['date'],
            result['result']['text_day'],
            result['result']['text_night'],
            result['result']["high"],
            result['result']["low"],
            result['result']["wind_direction"],
            result['result']["wind_speed"]
        )

    return text_message


def text_date_to_number_date(text_date):
    """
    讲user输入的str转化为API要求的数字格式
    免费账户：只能查询今天、明天、后天，三天的天气
    :param text_date:
    :return:
    """
    if text_date == "今天":
        return 0
    if text_date == "明天":
        return 1
    if text_date == "后天":
        return 2

    # Not supported by weather API provider freely
    if text_date == "大后天":
        # return 3
        return text_date

    if text_date.startswith("星期"):
        # @todo: using calender to compute relative date
        return text_date

    if text_date.startswith("下星期"):
        # @todo: using calender to compute relative date
        return text_date

    # follow APIs are not supported by weather API provider freely
    if text_date == "昨天":
        return text_date
    if text_date == "前天":
        return text_date
    if text_date == "大前天":
        return text_date



if __name__ == "__main__":

    # result = fetch_weather('北京', start=-3, days=10)
    result = get_result('北京朝阳', '今天', 2)

    print(result)

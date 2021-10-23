# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


import time
from typing import Dict, Text, Any, List

import requests
from rasa_sdk import Tracker, Action
from rasa_sdk.events import UserUtteranceReverted, AllSlotsReset, SlotSet
from rasa_sdk.executor import CollectingDispatcher


from actions.third_chat import *
from actions.express_search import *
from actions.weather_search import *


class ActionDefaultFallback(Action):
    """Executes the fallback action and goes back to the previous state
    of the dialogue"""

    def name(self):
        return 'action_default_fallback'

    def run(self, dispatcher, tracker, domain):

        # 访问图灵机器人API(闲聊)
        text = tracker.latest_message.get('text')
        message = get_response(text)
        if message is not None:
            dispatcher.utter_message('图灵bot：' + message)
        else:
            # dispatcher.utter_template('utter_default', tracker, silent_fail=True)
            dispatcher.utter_message(template='utter_default')
        return [UserUtteranceReverted()]


class ActionWhattodo(Action):

    def name(self) -> Text:
        return "action_whattodo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("我暂时支持的功能包括:\
                              查天气\
                              查快递\
                              闲聊")
        return []


class ActionSearchExpress(Action):
    def name(self) -> Text:
        return "action_search_express"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        express = tracker.get_slot('express_info')
        number = tracker.get_slot('number_info')

        express = express_list[express]
        response = get_express_response(express, number)
        datas = response.json()['data']
        message = ""
        for data in datas:
            time_info = data['time']
            context = data['context']
            message += f"时间：{time_info}\t" + f"物流状态：{context}\n"

        dispatcher.utter_message(text=message)

        return []


class ActionSearchWeather(Action):
    def name(self) -> Text:
        return "action_search_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        address = tracker.get_slot('address_info')
        date_time = tracker.get_slot('date_time_info')

        date_time = date_time[0] if isinstance(date_time, list) else date_time
        date_time_number = text_date_to_number_date(date_time)

        if isinstance(date_time_number, str):
            result = '抱歉，暂不支持查询{}的天气'.format(date_time_number)
            dispatcher.utter_message(result)
        else:
            result = get_result(address, date_time, date_time_number)
            dispatcher.utter_message(result)

        return [SlotSet("date_time_info", None), SlotSet("address_info", None)]

        # return {"express_info": None, "number_info": None}












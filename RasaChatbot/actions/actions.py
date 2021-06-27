# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests
from datetime import datetime
import unidecode

async def call_api_country(country):

    url = "https://covid-19-data.p.rapidapi.com/country"
    # today = datetime.today().strftime('%Y-%m-%d')
    querystring = {"name":country}

    headers = {
        'x-rapidapi-key': "71801fabf5msh40f5984b0dd783dp1d8bf4jsnf9b7577751fc",
        'x-rapidapi-host': "covid-19-data.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    if len(response.json()) == 0:
        return None
    else:
        return response.json()[0]

def remove_accent_char(text):
    res = unidecode.unidecode(text)
    return res

class ActionOverallCovidCountry(Action):

    def name(self) -> Text:
        return "overall_covid_country"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # text = tracker.latest_message['entities'][0]['value']
        text = tracker.latest_message['text']
        text = remove_accent_char(text)
        text = text.lower().replace(' ', '')

        if text == "ấnđộ":
            text = "India"
        elif text == "my" or text =="Mi" or text == "nuocmy":
            text = 'usa'
        elif text == 'ando':
            text = 'india'

        covid = await call_api_country(text)
        if covid is None:
            dispatcher.utter_message(text=f"Không có dữ liệu cho quốc gia này")
        else:
            dispatcher.utter_message(text=f"Có {covid['confirmed']} ca được xác nhận, {covid['recovered']} ca phục hồi, tử vong {covid['deaths']} người")
        return []
#
# class ActionGetWhereToGo(Action):
#
#     def name(self) -> Text:
#         return "get_where_to_go"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         location = tracker.get_slot("dia_diem")
#         if not location:
#             dispatcher.utter_message(text="Bạn chưa nói cho tôi là đi đâu?")
#         else:
#             dispatcher.utter_message(text=f"Bạn nói là đi {location} đúng không?")
#         return []
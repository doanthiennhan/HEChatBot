
import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from dotenv import load_dotenv
import os
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, ActionExecutionRejected
from getDatabase.get_room import *
load_dotenv()

BASE_URL = os.getenv("BASE_URL")

class ActionEventDetails(Action):

    def name(self) -> str:
        return "action_event_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get('text', '').lower()


        cultural_keywords = ["sự kiện văn hóa", "văn hóa", "truyền thống", "nghệ thuật", "lễ hội"]

        sport_keywords = ["thể thao", "bóng đá", "cầu lông", "chạy bộ"]

        entertainment_keywords = ["giải trí", "âm nhạc", "phim ảnh", "biểu diễn", "hài kịch"]


        event_types = set()  

        if any(keyword in user_message for keyword in cultural_keywords):
            event_types.add("văn hóa")
        if any(keyword in user_message for keyword in sport_keywords):
            event_types.add("thể thao")
        if any(keyword in user_message for keyword in entertainment_keywords):
            event_types.add("giải trí")

  
        print("Các loại sự kiện xác định:", list(event_types))

        all_events = []  
        combined_data = ""
 
        for event_type in event_types:
            search_query = event_type  
            page = 1  

            while True:
                url = f"{BASE_URL}blogs?page={page}&size=20&search={search_query}"
                try:
                    response = requests.get(url)
                    response.raise_for_status()  

                   
                    result = response.json().get("result", {})
                    events = result.get("data", [])
                    all_events.extend(events) 

                 
                    if result.get("currentPage") >= result.get("totalPages"):
                        break 

                    page += 1  
                except requests.exceptions.RequestException as e:
                    dispatcher.utter_message(template="utter_error")
                    return [ActionExecutionRejected(self.name())]

       
        unique_events = {event['id']: event for event in all_events}.values()

        
        if unique_events:
            event_list = "\n".join([f"- {event['title']}" for event in unique_events]) 
            combined_data = f"Các sự kiện của chúng tôi:\n{event_list}"
            return [SlotSet("combined_data", combined_data)]
        else:
            dispatcher.utter_message(text="Không tìm thấy sự kiện nào phù hợp.")
            return [ActionExecutionRejected(self.name())]
        
class ActionHikingTrails(Action):

    def name(self) -> Text:
        return "action_hiking_trails"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        return []
    
class ActionNightlife(Action):

    def name(self) -> Text:
        return "action_nightlife"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        return []

class ActionScenicDrives(Action):

    def name(self) -> Text:
        return "action_scenic_drives"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        return []

class ActionWaterActivities(Action):

    def name(self) -> Text:
        return "action_water_activities"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        

        return []

class ActionWildlifeSightings(Action):

    def name(self) -> Text:
        return "action_wildlife_sightings"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        return []


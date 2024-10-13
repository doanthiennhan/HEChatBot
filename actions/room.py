

import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from dotenv import load_dotenv
import os

from getDatabase.get_room import *

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
room_keywords = {
    "đơn": "Normal Room",
    "normal": "Normal Room",
    "đôi": "Family Room",
    "couple": "Couple Room",
    "family": "Family Room",
    "luxurious": "Luxurious Room",
    "president": "President Room",
    "vip": "President Room"
}



class ActionListRoomTypes(Action):

    def name(self) -> Text:
        return "action_list_room_types"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        result = get_room_type()
        if result:
            room_types = [room["name"] for room in result]
            response = "Các loại phòng hiện có là: " + ", ".join(room_types) + "."
        else:
            response = "Hiện không có thông tin về các loại phòng."

       
        dispatcher.utter_message(text=response)

        return []
    
class ActionGetRoomPrices(Action):

    def name(self) -> Text:
        return "action_get_room_prices"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

       
        room_types = get_room_type()

        if room_types:
           
            room_prices = {room["name"]: room["price"] for room in room_types}

       
            user_message = tracker.latest_message.get('text', '').lower()
            print(user_message)
            specific_room = next((room for keyword, room in room_keywords.items() if keyword in user_message), None)

        
            if specific_room and specific_room in room_prices:
                response = f"Giá của phòng {specific_room} là {room_prices[specific_room]:,} VNĐ."
            else:
                response = "Giá của tất cả các loại phòng là:\n"
                for room_name, price in room_prices.items():
                    response += f"- {room_name}: {price:,} VNĐ\n"  
        else:
            response = "Hiện không có thông tin về giá của các loại phòng."

       
        dispatcher.utter_message(text=response)

        return []


class ActionGetRoomDetails(Action):

    def name(self) -> Text:
        return "action_get_room_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

       
        room_details = get_room_type() 

        if room_details:
            room_info = {room["name"]: room["detail"] for room in room_details}

            user_message = tracker.latest_message.get('text', '').lower()
            print(user_message)
            specific_room = None

            for keyword, room in room_keywords.items():
                if keyword in user_message:
                    specific_room = room
                    break

         
            if specific_room and specific_room in room_info:
                response = f"Chi tiết của phòng {specific_room}: {room_info[specific_room]}"
            else:

                response = "Chi tiết của tất cả các loại phòng là:\n"
                for room_name, detail in room_info.items():
                    response += f"- {room_name}: {detail}\n"

        else:
            response = "Hiện không có thông tin về chi tiết các loại phòng."


        dispatcher.utter_message(text=response)

        return []

class ActionGetRoomCount(Action):
    def name(self) -> Text:
        return "action_get_room_count"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        room_count = len(get_room())
        
        dispatcher.utter_message(text=f"Tổng số phòng hiện mà khách sạn có là: {room_count}")
        return []
    
    
class ActionGetEmptyRooms(Action):
    def name(self) -> Text:
        return "action_get_empty_rooms"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
      
        empty_rooms = get_empty_room()
        
       
        if "error" in empty_rooms:
            response = empty_rooms["error"]
        else:
            if empty_rooms:
                response = "Danh sách phòng trống:\n" + "\n".join([f"Phòng số {room['roomNumber']} - Loại: {room['roomType']['name']}" for room in empty_rooms])
            else:
                response = "Hiện tại không có phòng nào trống."

        
        dispatcher.utter_message(text=response)
        
        return []
    

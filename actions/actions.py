# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

import random
import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from dotenv import load_dotenv
import os
from rasa_sdk.types import DomainDict
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

class ActionListServices(Action):

    def name(self) -> Text:
        return "action_list_services"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Lấy câu hỏi người dùng từ tracker
        user_question = tracker.latest_message.get('text')
        
        # In ra câu hỏi của người dùng (có thể sử dụng print hoặc logging)
        print(f"Người dùng đã hỏi: {user_question}")
        # URL của API
        url = BASE_URL + "serviceTypes"
        
        try:
            # Gửi yêu cầu GET đến API
            response = requests.get(url)
            response.raise_for_status()  # Kiểm tra mã trạng thái HTTP

            data = response.json()

            if "result" in data and isinstance(data["result"], list):
                services = data["result"]
                num_services = len(services)
                
                # Liệt kê các dịch vụ
                service_list = ", ".join([service["name"] for service in services])
                
                # Tạo phản hồi cho người dùng
                message = f"Hiện tại có {num_services} loại dịch vụ: {service_list}."
            else:
                message = "Không tìm thấy dữ liệu về dịch vụ."
        
        except requests.exceptions.RequestException as e:
            # Bắt lỗi khi có sự cố với yêu cầu
            
            message = f"Xin lỗi . tôi không thể trả lời câu hỏi này của bạn "
        
        dispatcher.utter_message(text=message)

        return []
    
class ActionEventDetails(Action):

    def name(self) -> str:
        return "action_event_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict):

        # Lấy câu hỏi của người dùng
        user_message = tracker.latest_message.get('text', '').lower()

        # Từ khóa sự kiện văn hóa
        cultural_keywords = ["sự kiện văn hóa", "văn hóa", "truyền thống", "nghệ thuật", "lễ hội"]
        # Từ khóa sự kiện thể thao
        sport_keywords = ["thể thao", "bóng đá", "cầu lông", "chạy bộ"]
        # Từ khóa sự kiện giải trí
        entertainment_keywords = ["giải trí", "âm nhạc", "phim ảnh", "biểu diễn", "hài kịch"]

        # Xác định loại sự kiện dựa trên từ khóa
        event_types = set()  # Sử dụng set để lưu trữ các loại sự kiện duy nhất

        if any(keyword in user_message for keyword in cultural_keywords):
            event_types.add("văn hóa")
        if any(keyword in user_message for keyword in sport_keywords):
            event_types.add("thể thao")
        if any(keyword in user_message for keyword in entertainment_keywords):
            event_types.add("giải trí")

        # In ra các loại sự kiện đã xác định
        print("Các loại sự kiện xác định:", list(event_types))

        return []
    

class ActionPrintUserQuestion(Action):
    def name(self) -> Text:
        return "action_print_user_question"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Lấy câu hỏi người dùng từ tracker
        user_question = tracker.latest_message.get('text')
        
        # In ra câu hỏi của người dùng (có thể sử dụng print hoặc logging)
        print(f"Người dùng đã hỏi: {user_question}")
        
        # Phản hồi lại người dùng bằng chính câu hỏi đó
        dispatcher.utter_message(text=f"Bạn đã hỏi: {user_question}")
        
        return []



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

        # Gửi thông báo đến người dùng
        dispatcher.utter_message(text=response)

        return []
    
class ActionGetRoomPrices(Action):

    def name(self) -> Text:
        return "action_get_room_prices"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Lấy dữ liệu từ API hoặc hàm `get_ticket_prices()`
        room_types = get_room_type()

        if room_types:
            # Tạo một từ điển chứa tên phòng và giá của chúng
            room_prices = {room["name"]: room["price"] for room in room_types}

            # Lấy tin nhắn của người dùng và chuyển thành chữ thường để so sánh
            user_message = tracker.latest_message.get('text', '').lower()
            print(user_message)
            specific_room = next((room for keyword, room in room_keywords.items() if keyword in user_message), None)

            # Trả về giá của một loại phòng cụ thể nếu tìm thấy từ khóa
            if specific_room and specific_room in room_prices:
                response = f"Giá của phòng {specific_room} là {room_prices[specific_room]:,} VNĐ."
            else:
                response = "Giá của tất cả các loại phòng là:\n"
                for room_name, price in room_prices.items():
                    response += f"- {room_name}: {price:,} VNĐ\n"  
        else:
            response = "Hiện không có thông tin về giá của các loại phòng."

        # Gửi thông báo đến người dùng
        dispatcher.utter_message(text=response)

        return []

class ActionGetRoomDetails(Action):

    def name(self) -> Text:
        return "action_get_room_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Giả sử bạn có một hàm để lấy chi tiết phòng từ API hoặc cơ sở dữ liệu
        room_details = get_room_type()  # Thay thế bằng hàm thật của bạn

        if room_details:
            room_info = {room["name"]: room["detail"] for room in room_details}

            user_message = tracker.latest_message.get('text', '').lower()
            print(user_message)
            # Khai báo biến để lưu tên phòng cụ thể
            specific_room = None

            for keyword, room in room_keywords.items():
                if keyword in user_message:
                    specific_room = room
                    break

            # Trả về chi tiết của phòng cụ thể nếu tìm thấy
            if specific_room and specific_room in room_info:
                response = f"Chi tiết của phòng {specific_room}: {room_info[specific_room]}"
            else:
                # Trả về chi tiết của tất cả các loại phòng nếu không tìm thấy phòng cụ thể
                response = "Chi tiết của tất cả các loại phòng là:\n"
                for room_name, detail in room_info.items():
                    response += f"- {room_name}: {detail}\n"

        else:
            response = "Hiện không có thông tin về chi tiết các loại phòng."

        # Gửi thông báo đến người dùng
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
        
        # Gọi hàm get_empty_room để lấy danh sách phòng trống
        empty_rooms = get_empty_room()
        
        # Kiểm tra và xử lý kết quả
        if "error" in empty_rooms:
            response = empty_rooms["error"]
        else:
            if empty_rooms:
                response = "Danh sách phòng trống:\n" + "\n".join([f"Phòng số {room['roomNumber']} - Loại: {room['roomType']['name']}" for room in empty_rooms])
            else:
                response = "Hiện tại không có phòng nào trống."

        # Gửi thông báo đến người dùng
        dispatcher.utter_message(text=response)
        
        return []
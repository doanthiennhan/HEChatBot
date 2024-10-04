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
load_dotenv()

BASE_URL = os.getenv("BASE_URL")

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

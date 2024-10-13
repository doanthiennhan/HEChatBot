import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from dotenv import load_dotenv
import os
from rasa_sdk.events import SlotSet, ActionExecutionRejected
from getDatabase.get_room import *
load_dotenv()

BASE_URL = os.getenv("BASE_URL")

def get_current_intent(tracker): 
    return tracker.latest_message['intent'].get('name')

class ActionGetReturnFAQ(Action):
    def name(self) -> Text:
        return "action_get_return_faq"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        combined_data = ""
        intent = get_current_intent(tracker)
        print("intent: ", intent)
        try:
            response = requests.get(BASE_URL + "faq/"+intent)
            response.raise_for_status()  
            data = response.json()
            description = data['result']['description']
            combined_data = f"{description}"
            print(combined_data)
            
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(template="utter_error")
            return [ActionExecutionRejected(self.name())]
    
        return [SlotSet("combined_data", combined_data)]
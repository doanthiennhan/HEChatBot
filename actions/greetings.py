import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from dotenv import load_dotenv
from rasa_sdk.events import SlotSet, ActionExecutionRejected
import os

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

class ActionGreet(Action):
    def name(self) -> Text:
        return "action_set_user_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_name = tracker.get_latest_entity_values("name", None)
        if user_name:
            return [SlotSet("combined_data", user_name)]
        return []
# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from actions import database_connectivity

from database_connectivity import Database

class addItemSubmit(Action):

    def name(self) -> Text:
        return "action_add_item"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        activity = tracker.get_slot("activity")
        category = tracker.get_slot("category")
        deadline = tracker.get_slot("deadline")

        dispatcher.utter_message(text=f"Congratulation, {activity} added to {category}, complete before {deadline}") 
        
        Database.DataUpdate("facility_type","location")
        

        return [SlotSet("activity", None),SlotSet("category", None),SlotSet("deadline",None)]
        

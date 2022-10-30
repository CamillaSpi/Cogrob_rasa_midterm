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

from . import Database

class actionAddItem(Action):

    def name(self) -> Text:
        return "action_add_item"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        username = tracker.get_slot("username")
        username = "Nando"
        activity = tracker.get_slot("activity")
        category = tracker.get_slot("category")
        deadline = tracker.get_slot("deadline")

        dispatcher.utter_message(text=f"Congratulation {username}, {activity} added to {category}, complete before {deadline}") 
        
        Database.insertItem(username,activity ,category,deadline)
        

        return [SlotSet("activity", None),SlotSet("category", None),SlotSet("deadline",None)]

class actionRemoveItem(Action):

    def name(self) -> Text:
        return "action_remove_item"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: 
        username = tracker.get_slot("username")
        username = "Nando"
        activity = tracker.get_slot("activity")
        category = tracker.get_slot("category")
        deadline = tracker.get_slot("deadline")

        dispatcher.utter_message(text=f"Congratulation {username}, {activity} remove from {category}") 
        
        Database.deleteItem(username,activity ,category,deadline)
        

        return [SlotSet("activity", None),SlotSet("category", None),SlotSet("deadline",None)]
            

class actionAddCategory(Action):

    def name(self) -> Text:
        return "action_add_category"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: 
        username = tracker.get_slot("username")
        username = "Nando"
        category = tracker.get_slot("category")

        dispatcher.utter_message(text=f"Congratulation {username}, {category} added as a new Category") 
        
        Database.insertCategory(username,category)
        

        return [SlotSet("category", None)]
            

class actionRemoveCategory(Action):

    def name(self) -> Text:
        return "action_remove_category"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: 
        
        username = tracker.get_slot("username")
        username = "Nando"
        category = tracker.get_slot("category")

        dispatcher.utter_message(text=f"Congratulation {username}, {category} removed from your Category") 
        
        Database.deleteCategory(username,category)
        

        return [SlotSet("category", None)]

class actionSetComplete(Action):

    def name(self) -> Text:
        return "action_set_complete"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        username = tracker.get_slot("username")
        username = "Nando"
        activity = tracker.get_slot("activity")
        category = tracker.get_slot("category")
        deadline = tracker.get_slot("deadline")

        dispatcher.utter_message(text=f"Congratulation {username}, {activity} in {category} completed !") 
        
        Database.setItemStatus(username,activity ,category,deadline,True)
        

        return [SlotSet("activity", None),SlotSet("category", None),SlotSet("deadline",None)]

class actionSetInComplete(Action):

    def name(self) -> Text:
        return "action_set_uncomplete"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        username = tracker.get_slot("username")
        username = "Nando"
        activity = tracker.get_slot("activity")
        category = tracker.get_slot("category")
        deadline = tracker.get_slot("deadline")

        dispatcher.utter_message(text=f"Congratulation {username}, {activity} in {category} set as incompleted !") 
        
        Database.setItemStatus(username,activity ,category,deadline,False)
        

        return [SlotSet("activity", None),SlotSet("category", None),SlotSet("deadline",None)]

class wantActivitiesForm(Action):
    def name(self) -> Text:
        return "action_want_activities"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        username = tracker.get_slot("username")
        username = "Nando"

        dispatcher.utter_message(text=f"This are all your activities: {Database.selectItems(username)}") 

        return 
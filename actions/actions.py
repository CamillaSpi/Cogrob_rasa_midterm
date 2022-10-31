# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from unicodedata import category

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from . import Database

class actionCreateUser(Action):

    def name(self) -> Text:
        return "action_create_user"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        username = tracker.get_slot("username")
        name = tracker.get_slot("name")
                
        returnedValue= Database.createUser(username,name)

        if (returnedValue):  
            dispatcher.utter_message(text=f"Congratulation {name}, or i should call you {username} :P {returnedValue}") 
        else:
            dispatcher.utter_message(text=f"Ops! {username} something went wrong, I'm so triste for that :(") 

        return []


class actionAddItem(Action):

    def name(self) -> Text:
        return "action_add_item"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        username = tracker.get_slot("username")
        activity = tracker.get_slot("activity")
        category = tracker.get_slot("category")
        deadline = tracker.get_slot("deadline")
        
        returnedValue= Database.insertItem(username,activity ,category,deadline)

        if (returnedValue):  
            dispatcher.utter_message(text=f"Congratulation {username}, {activity} added to {category}, complete before {deadline}") 
        else:
            dispatcher.utter_message(text=f"Ops! {username} something went wrong, I'm so triste for that :(") 
        

        return [SlotSet("activity", None),SlotSet("category", None),SlotSet("deadline",None)]

class actionRemoveItem(Action):

    def name(self) -> Text:
        return "action_remove_item"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: 
        username = tracker.get_slot("username")
        activity = tracker.get_slot("activity")
        category = tracker.get_slot("category")
        deadline = tracker.get_slot("deadline")

        
        returnedValue = Database.deleteItem(username,activity ,category,deadline)

        if (returnedValue):  
            dispatcher.utter_message(text=f"Congratulation {username}, {activity} remove from {category}") 
        else:
            dispatcher.utter_message(text=f"Ops! {username} something went wrong, I'm so triste for that :(") 
        

        return [SlotSet("activity", None),SlotSet("category", None),SlotSet("deadline",None)]
            

class actionAddCategory(Action):

    def name(self) -> Text:
        return "action_add_category"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: 
        username = tracker.get_slot("username")
        category = tracker.get_slot("category")

        returnedValue = Database.insertCategory(username,category)
        if (returnedValue):  
            dispatcher.utter_message(text=f"Congratulation {username}, {category} added as a new Category") 
        else:
            dispatcher.utter_message(text=f"Ops! {username} something went wrong, I'm so triste for that :(") 


        return [SlotSet("category", None)]
            

class actionRemoveCategory(Action):

    def name(self) -> Text:
        return "action_remove_category"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: 
        
        username = tracker.get_slot("username")
        category = tracker.get_slot("category")

        
        returnedValue = Database.deleteCategory(username,category)
        if (returnedValue):  
            dispatcher.utter_message(text=f"Congratulation {username}, category {category} removed") 
        else:
            dispatcher.utter_message(text=f"Ops! {username} something went wrong, I'm so triste for that :(") 
        

        return [SlotSet("category", None)]

class actionSetComplete(Action):

    def name(self) -> Text:
        return "action_set_complete"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        username = tracker.get_slot("username")
        activity = tracker.get_slot("activity")
        category = tracker.get_slot("category")
        deadline = tracker.get_slot("deadline")

        
        returnedValue = Database.setItemStatus(username,activity ,category,deadline,True)

        if (returnedValue):  
            dispatcher.utter_message(text=f"Congratulation {username}, {activity} in {category} completed !") 
        else:
            dispatcher.utter_message(text=f"Ops! {username} something went wrong, I'm so triste for that :(") 
        

        return [SlotSet("activity", None),SlotSet("category", None),SlotSet("deadline",None)]

class actionSetInComplete(Action):

    def name(self) -> Text:
        return "action_set_uncomplete"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        username = tracker.get_slot("username")
        activity = tracker.get_slot("activity")
        category = tracker.get_slot("category")
        deadline = tracker.get_slot("deadline")

          
        returnedValue = Database.setItemStatus(username,activity ,category,deadline,False)

        if (returnedValue):  
            dispatcher.utter_message(text=f"Congratulation {username}, {activity} in {category} set as incompleted !") 
        else:
            dispatcher.utter_message(text=f"Ops! {username} something went wrong, I'm so triste for that :(") 
        

        return [SlotSet("activity", None),SlotSet("category", None),SlotSet("deadline",None)]

class wantActivitiesForm(Action):
    def name(self) -> Text:
        return "action_view_activities"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        username = tracker.get_slot("username")
        category = tracker.get_slot("category")

        dispatcher.utter_message(text=f"This are all your activities:\n{Database.selectItems(username,category)}") 

        return 
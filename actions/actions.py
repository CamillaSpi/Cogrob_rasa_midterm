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
        
        if(Database.doesUserExists(username) == False):
            returnedValue = Database.createUser(username)
            if(returnedValue):
                dispatcher.utter_message(text=f"Congratulation {username} your account has been correctly created:P") 
            else:
                dispatcher.utter_message(text=f"Oh no {username} your account already exists")
        else:
            dispatcher.utter_message(text=f"Congratulation {username} you're logged in!!!") 
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
        reminder = tracker.get_slot("reminder")
        time = tracker.get_slot("time")
        if(time != None and len(time) == 2):
            time = time['to']

        if(Database.doesUserExists(username)):
            if(Database.doesPossessionExists(username,category)):
                returnedValue= Database.insertItem(username,activity ,category,reminder,time)
                if (returnedValue):  
                    text = f"Congratulation {username}, {activity} added to {category}" + (f", complete before {time[:10]} at {time[11:16]}." if time else ".") + (" I will remind you, dont worry :P " if reminder else "") 
                    dispatcher.utter_message(text=text) 
                else:
                    dispatcher.utter_message(text=f"Ops! {username} something went wrong, you already inserted this activity :(") 
            else:
                dispatcher.utter_message(text=f"The category does not exists! I'm creating it!") 
                actionAddCategory.run(self, dispatcher,tracker,domain)
                actionAddItem.run(self, dispatcher,tracker,domain)
        else:
            dispatcher.utter_message(text=f"This username does not exists!") 
            return [SlotSet("username",None),SlotSet("activity", None),SlotSet("category", None), SlotSet("reminder",False), SlotSet("time",None)]

        return [SlotSet("activity", None),SlotSet("category", None),SlotSet("time",None),SlotSet("reminder",False)]

class actionRemoveItem(Action):

    def name(self) -> Text:
        return "action_remove_item"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: 
        username = tracker.get_slot("username")
        activity = tracker.get_slot("activity")
        category = tracker.get_slot("category")
        time = tracker.get_slot("time")

        
        if(Database.doesUserExists(username)):
            returnedValue = Database.deleteItem(username,activity ,category,time)

            if (returnedValue):  
                dispatcher.utter_message(text=f"Congratulation {username}, {activity} removed from {category}") 
            else:
                dispatcher.utter_message(text=f"Ops! {username} something went wrong, I didn't find this activity :(") 

        else:
            dispatcher.utter_message(text=f"This username does not exists!") 
            return [SlotSet("username",None),SlotSet("activity", None),SlotSet("category", None),SlotSet("time",None)]

        return [SlotSet("activity", None),SlotSet("category", None),SlotSet("time",None)]
            

class actionAddCategory(Action):

    def name(self) -> Text:
        return "action_add_category"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: 
        username = tracker.get_slot("username")
        category = tracker.get_slot("category")

        if(Database.doesUserExists(username)):
            returnedValue = Database.insertCategory(username,category)
            if (returnedValue):  
                dispatcher.utter_message(text=f"Congratulation {username}, {category} added as a new Category") 
            else:
                dispatcher.utter_message(text=f"Ops! {username} something went wrong, you already inserted this category") 

        else:
            dispatcher.utter_message(text=f"This username does not exists!") 
            return [SlotSet("username",None),SlotSet("category", None)]

        return [SlotSet("category", None)]
            

class actionRemoveCategory(Action):

    def name(self) -> Text:
        return "action_remove_category"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: 
        
        username = tracker.get_slot("username")
        category = tracker.get_slot("category")

        
        if(Database.doesUserExists(username)):
            returnedValue = Database.deleteCategory(username,category)
            if (returnedValue):  
                dispatcher.utter_message(text=f"Congratulation {username}, category {category} removed") 
            else:
                dispatcher.utter_message(text=f"Ops! {username} something went wrong,I didn't find this category :(") 

        else:
            dispatcher.utter_message(text=f"This username does not exists!") 
            return [SlotSet("username",None),SlotSet("category", None)]

        return [SlotSet("category", None)]

class actionSetStatusActivity(Action):

    def name(self) -> Text:
        return "action_set_status_activity"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        username = tracker.get_slot("username")
        activity = tracker.get_slot("activity")
        category = tracker.get_slot("category")
        activity_status = tracker.get_slot("activity_status")
        time = tracker.get_slot("time")

        
        if(Database.doesUserExists(username)):
            if activity_status == 'completed':
                returnedValue = Database.setItemStatus(username,activity ,category,time,True)
            elif activity_status == 'uncompleted':
                returnedValue = Database.setItemStatus(username,activity ,category,time,False)
            else:
                dispatcher.utter_message(text=f"Ops! {username} something went wrong, I didn't understand what u want to do with this activity :(") 
                return [SlotSet("activity", None),SlotSet("category", None),SlotSet("time",None),SlotSet("activity_status",None)]

            if (returnedValue):  
                dispatcher.utter_message(text=f"Congratulation {username}, {activity} in {category} set as {activity_status} !") 
            else:
                dispatcher.utter_message(text=f"Ops! {username} something went wrong, I didn't find this activity :(") 

        else:
            dispatcher.utter_message(text=f"This username does not exists!") 
            return [SlotSet("username",None),SlotSet("activity", None),SlotSet("category", None),SlotSet("time",None),SlotSet("activity_status",None)]

        return [SlotSet("activity", None),SlotSet("category", None),SlotSet("time",None),SlotSet("activity_status",None)]

class actionSetInComplete(Action):

    def name(self) -> Text:
        return "action_set_uncomplete"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        username = tracker.get_slot("username")
        activity = tracker.get_slot("activity")
        category = tracker.get_slot("category")
        time = tracker.get_slot("time")

          
        if(Database.doesUserExists(username)):
            returnedValue = Database.setItemStatus(username,activity ,category,time,False)

            if (returnedValue):  
                dispatcher.utter_message(text=f"Congratulation {username}, {activity} in {category} set as incompleted !") 
            else:
                dispatcher.utter_message(text=f"Ops! {username} something went wrong, I didn't find this activity :(") 

        else:
            dispatcher.utter_message(text=f"This username does not exists!") 
            return [SlotSet("username",None),SlotSet("activity", None),SlotSet("category", None),SlotSet("time",None),SlotSet("activity_status",None)]

        return [SlotSet("activity", None),SlotSet("category", None),SlotSet("time",None),SlotSet("activity_status",None)]

class showActivities(Action):
    def name(self) -> Text:
        return "action_view_activities"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        username = tracker.get_slot("username")
        category = tracker.get_slot("category")
        activity_status = tracker.get_slot("activity_status")

        if(Database.doesUserExists(username)):
            list_of_activity = Database.selectItems(username,category, activity_status)
            dispatcher.utter_message(text=(f"This are the requested activity:\n{list_of_activity}" if list_of_activity else "No activity found!")) 
        else:
            dispatcher.utter_message(text=f"This username does not exists!") 
            return [SlotSet("username",None),SlotSet("category", None),SlotSet("activity_status", None)]

        return [SlotSet("category", None),SlotSet("activity_status", None)]

class showCategories(Action):
    def name(self) -> Text:
        return "action_view_categories"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        username = tracker.get_slot("username")

        if(Database.doesUserExists(username)):
            dispatcher.utter_message(text=f"These are all your categories:\n{Database.selectCategories(username)}") 
        else:
            dispatcher.utter_message(text=f"This username does not exists!") 
            return [SlotSet("username",None), SlotSet("activity", None)]

        return [SlotSet("activity", None)]

class actionModifyCategory(Action):
    def name(self) -> Text:
        return "action_modify_category"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        username = tracker.get_slot("username")
        category_old = tracker.get_slot("category_old")
        category_new = tracker.get_slot("category")
        
        if(Database.doesUserExists(username)):
            if (Database.doesPossessionExists(username,category_new) == False):

                returnedValue = Database.modifyCategory(username, category_old, category_new)
                if (returnedValue):  
                    dispatcher.utter_message(text=f"Congratulation {username}, {category_old} modified in {category_new} !") 
                else:
                    dispatcher.utter_message(text=f"Ops! {username} something went wrong, I didn't find this category :(") 
            else:
                dispatcher.utter_message(text=f"Ops! {username} the {category_new} already exists!") 
        else:
            dispatcher.utter_message(text=f"This username does not exists!") 
            return [SlotSet("username",None),SlotSet("category_old", None),SlotSet("category", None)]
        return [SlotSet("category_old", None),SlotSet("category", None)]

class actionModifyActivity(Action):
    def name(self) -> Text:
        return "action_modify_activity"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        possibleDeadlineErrorFlag=False
        username = tracker.get_slot("username")
        category_old = tracker.get_slot("category_old")
        activity_old = tracker.get_slot("activity_old")
        activity_new = tracker.get_slot("activity")
        category_new = tracker.get_slot("category")
        time = tracker.get_slot("time")
        if(time != None and len(time) == 2 and not isinstance(time, list)):
            print("sono entrato nel primo if")
            timenew = time['to']
            timeold = time['from']
        elif(isinstance(time, list)):
            print("sono entrato nel primo elsif")
            timeold = time[0]['from']
            timenew = time[1]
        elif(Database.doesUnfoldingsExists(username,category_old,activity_old)): 
            print("sono entrato nel secondo elsif")
            timenew = time
            timeold = None
        else:
            print("sono entrato nell else", activity_new,category_new)
            possibleDeadlineErrorFlag=True
            timenew = time
            timeold = time
        if possibleDeadlineErrorFlag is True and activity_new is None and category_new is None:
            print("sono nel possibleDead")
            dispatcher.utter_message(text=f"please insert old and new deadline in the next request to allow me to change the deadline of the activity!!")
            return [SlotSet("category_old", None),SlotSet("activity_old", None),SlotSet("time", None)]
        
        if(activity_new!=None):
            act_to_query = activity_new
        else:
            act_to_query = activity_old
        if(category_new!=None):
            cat_to_query = category_new
        else:
            cat_to_query = category_old

        if(Database.doesUserExists(username)):
            if (Database.doesUnfoldingsExists(username,cat_to_query,act_to_query,timenew) == False):
                returnedValue = Database.modifyActivity(username, category_old, activity_old, timeold, category_new, activity_new, timenew)
                if (returnedValue):  
                    dispatcher.utter_message(text=f"Congratulation {username}, the activity {act_to_query} has been updated !") 
                else:
                    dispatcher.utter_message(text=f"Ops! {username} something went wrong, I didn't find the activity to be updated :(") 
            else:
                dispatcher.utter_message(text=f"Ops! {username} the {activity_old} already exists, it makes no sense to update that!") 
        else:
            dispatcher.utter_message(text=f"This username does not exists!") 
            return [SlotSet("username",None),SlotSet("category_old", None),SlotSet("activity_old", None),SlotSet("time", None),SlotSet("category", None),SlotSet("activity", None)]
        return [SlotSet("category_old", None),SlotSet("activity_old", None),SlotSet("time", None),SlotSet("category", None),SlotSet("activity", None)]


class actionSetReminderSlot(Action):
    def name(self) -> Text:
        return "action_set_reminder_slot"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return[SlotSet("reminder",True)]


class actionCleanCompletedActivities(Action):
    def name(self) -> Text:
        return "action_clean_all_completed"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        username = tracker.get_slot("username")          
        if(Database.doesUserExists(username)):
            returnedValue = Database.cleanCompletedActivities(username)
            if (returnedValue):  
                dispatcher.utter_message(text=f"Congratulation {username}, I've removed all you completed activity !") 
            else:
                dispatcher.utter_message(text=f"Ops! {username} something went wrong! I dont know, check it !")
        else:
            dispatcher.utter_message(text=f"This username does not exists!") 
            return [SlotSet("username",None)]
        return []

class actionResetSlot(Action):
    def name(self) -> Text:
        return "action_reset_slot"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        
        return [SlotSet("activity_old",None),
        SlotSet("activity",None),
        SlotSet("category_old",None),
        SlotSet("category",None),
        SlotSet("time",None),
        SlotSet("activity_status",None)
        ]



class actionRemindItem(Action):
    def name(self) -> Text:
        return "action_reminder_item"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        username = tracker.get_slot("username")
        activity = tracker.get_slot("activity")
        category = tracker.get_slot("category")
        reminder = tracker.get_slot("reminder")
        time = tracker.get_slot("time")

        # check if exist and then update
        if (Database.doesUnfoldingsExists(username,category,activity,time)):
            Database.updateReminder(username,category,activity,time,reminder)
        else:
            actionAddItem.run(self,dispatcher,tracker,domain)
        #else call add item

        
        

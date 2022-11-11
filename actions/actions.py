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
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict
from datetime import datetime, timedelta

from . import Database

class actionCreateUser(Action):

    def name(self) -> Text:
        return "action_recognize_user"

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
            returnedValue = Database.insertCategoryAndPossession(username,category)
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
            dispatcher.utter_message(text=f"These are all your categories:\n{Database.selectPossessions(username)}") 
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
        category_new = tracker.get_slot("category_new")
        
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
            return [SlotSet("username",None),SlotSet("category_old", None),SlotSet("category_new", None),SlotSet("category", None)]
        return [SlotSet("category_old", None),SlotSet("category_new", None),SlotSet("category", None)]

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
        activity_new = tracker.get_slot("activity_new")
        category_new = tracker.get_slot("category_new")
        category = tracker.get_slot("category")
        activity = tracker.get_slot("activity")
        time = tracker.get_slot("time")
       
        if(activity_old!=None):
            act_to_modify = activity_old
        else:
            act_to_modify = activity
        if(category_old!=None):
            cat_to_modify = category_old
        else:
            cat_to_modify = category
        
        if(time != None and len(time) == 2 and not isinstance(time, list)):
            if(time['to'] != None):
                tmp = str(datetime.strptime(time['to'], "%Y-%m-%dT%H:%M:%S.%f%z") - timedelta(days=1)).split(" ")
                timenew = tmp[0] + "T" + (tmp[1])[:-6] + ".000" + (tmp[1])[-6:]
                
            else:
                timenew = time['from'] 
            timeold = time['from']
        elif(isinstance(time, list)):
            timeold = time[0]['from']
            timenew = time[1]
        elif(Database.doesUnfoldingsExists(username,category,activity) and category_new == None and activity_new == None):
            
            timenew = time
            timeold = None
        else:
            possibleDeadlineErrorFlag=True
           
            timenew = time
            timeold = time
        if possibleDeadlineErrorFlag is True and activity_old is None and category_old is None:
            dispatcher.utter_message(text=f"please insert old and new deadline in the next request to allow me to change the deadline of the activity!!")
            return [SlotSet("category", None),SlotSet("category_old", None),SlotSet("activity_old", None),SlotSet("category_new", None),SlotSet("activity_new", None),SlotSet("activity", None),SlotSet("time", None)]
    

        if(category_new == None):
            category_new = category
        if(activity_new == None):
            activity_new = activity
        if(Database.doesUserExists(username)):
            if (Database.doesUnfoldingsExists(username,category_new,activity_new,timenew) == False):
                returnedValue = Database.modifyActivity(username, cat_to_modify, act_to_modify, timeold, category_new, activity_new, timenew)
                if (returnedValue):  
                    dispatcher.utter_message(text=f"Congratulation {username}, the activity {act_to_modify} has been updated !") 
                else:
                    dispatcher.utter_message(text=f"Ops! {username} something went wrong, I didn't find the activity to be updated :(") 
            else:
                dispatcher.utter_message(text=f"Ops! {username} the {act_to_modify} already exists, it makes no sense to update that!") 
        else:
            dispatcher.utter_message(text=f"This username does not exists!") 
            return [SlotSet("username", None),SlotSet("category_old", None),SlotSet("activity_old", None),SlotSet("time", None),SlotSet("category_new", None),SlotSet("activity_new", None),SlotSet("category", None),SlotSet("activity", None)]
        return [SlotSet("category_old", None),SlotSet("activity_old", None),SlotSet("time", None),SlotSet("category_new", None),SlotSet("activity_new", None),SlotSet("category", None),SlotSet("activity", None)]


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

        if (Database.doesUnfoldingsExists(username,category,activity,time)):
            
            returnedValue = Database.updateReminder(username,category,activity,time,reminder)
            if (returnedValue):
                dispatcher.utter_message(text=f"Activity Updated!")
            else:
                dispatcher.utter_message(text=f"Soome problem with the update occurred!")
        else:
            actionAddItem.run(self,dispatcher,tracker,domain)
        
        return [SlotSet("activity",None), SlotSet("time",None), SlotSet("category",None),SlotSet("reminder",False)]



class actionAskCategoryOld(Action):
    def name(self) -> Text:
        return "action_ask_category_old"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        category_old = tracker.get_slot("category_old")
        category = tracker.get_slot("category")
        if(category_old == None and category == None):
            dispatcher.utter_message(text=f"Please insert the category to be modified")
            return[SlotSet("requested_slot","category")]
        else:
            dispatcher.utter_message(text=f"Please insert the category new")
            return[SlotSet("category_old",category),SlotSet("category",None),SlotSet("category_new",None),SlotSet("requested_slot","category")]    
        


class actionAskCategoryNew(Action):
    def name(self) -> Text:
        return "action_ask_category_new"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        category_new = tracker.get_slot("category_new")
        category = tracker.get_slot("category")
        if(category_new == None and category == None):
            dispatcher.utter_message(text=f"Please insert the category new")
            return[SlotSet("requested_slot","category")]
        else:
            return[SlotSet("category_new",category),SlotSet("category",None),SlotSet("requested_slot",None)]    
        

class actionAskActivityOld(Action):
    def name(self) -> Text:
        return "action_ask_activity_old"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        activity_old = tracker.get_slot("activity_old")
        activity = tracker.get_slot("activity")
        if(activity_old == None and activity == None):
            dispatcher.utter_message(text=f"Please insert the activity to be modified")
            return[SlotSet("requested_slot","activity")]
        else:
            dispatcher.utter_message(text=f"Please insert the activity new")
            return[SlotSet("activity_old",activity),SlotSet("activity",None),SlotSet("activity_new",None),SlotSet("requested_slot","activity")]    

class actionAskActivityNew(Action):
    def name(self) -> Text:
        return "action_ask_activity_new"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        activity_new = tracker.get_slot("activity_new")
        activity = tracker.get_slot("activity")
        if(activity_new == None and activity == None):
            dispatcher.utter_message(text=f"Please insert the activity new")
            return[SlotSet("requested_slot","activity")]
        else:
            return[SlotSet("activity_new",activity),SlotSet("activity",None),SlotSet("requested_slot",None)]    
        



class actionDefaultFallBack(Action):
    def name(self) -> Text:
        return "my_action_fallback"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=f"Sorry, I lost my mind!")    
        return [SlotSet("activity_old",None),
        SlotSet("activity",None),
        SlotSet("category_old",None),
        SlotSet("category",None),
        SlotSet("time",None),
        SlotSet("activity_status",None),
        SlotSet("activity_new",None),
        SlotSet("category_new",None)]

# class ValidateModifyCategoryForm(FormValidationAction):
#     def name(self) -> Text:
#         return "validate_modify_category_form"

#     def validate_category_old(
#         self,
#         value: Text,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: DomainDict,
#     ) -> Dict[Text, Any]:

#         dispatcher.utter_message(text=f"Alfredo")

#     def validate_category(
#         self,
#         value: Text,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: DomainDict,
#     ) -> Dict[Text, Any]:

#         dispatcher.utter_message(text=f"Mario")

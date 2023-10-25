import requests
from rasa_sdk.events import SlotSet
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import FollowupAction
from langid.langid import LanguageIdentifier, model
from googletrans import Translator


class ActionGreet(Action):
    def name(self) -> Text:
        return "action_greet"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        message = "Dear Customer, welcome to ABC GROUP. How can I assist you today?"
        buttons = [
            {"title": "PF", "id": "/PF"},
            {"title": "Payroll&Attendance", "id": "/Payroll_Att"},
            {"title": "Reimbursement", "id": "/Reimbursement"},
            {"title": "Language Options", "id": "/Language_Opt"},
            {"title": "Exit", "id": "/goodbye"}
        ]
        user_lang = 'en'  # default to English
        lang_identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)
        detected_lang, confidence = lang_identifier.classify(tracker.latest_message['text'])
        if confidence > 0.5:
            user_lang = detected_lang
        translator = Translator()
        if user_lang == "en":
            translated_msg = message
            translated_buttons = buttons
        else:
            try:
                translated_msg = translator.translate(message, dest=user_lang).text
                translated_buttons = []
                for button in buttons:
                    translated_title = translator.translate(button['title'], dest=user_lang).text
                    translated_buttons.append({"title": translated_title, "id": button["id"]})
            except:
                translated_msg = message  
                translated_buttons = buttons
        dispatcher.utter_message(text=translated_msg, buttons=translated_buttons)
        return [SlotSet("language", user_lang)]

class ActionLanguageMenu(Action):
    def name(self) -> Text:
        return "action_language"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # get the language slot value from the tracker
        language = tracker.slots.get("language")
        
        # translate the message if the language is not English
        if language != "en":
            translator = Translator()
            message = translator.translate("Please select your preferred language:", dest=language).text
        else:
            message = "Please select your preferred language:"
        
        # translate the button titles
        buttons = [
            {"title": "English", "id": "en"},
            {"title": "Malayalam", "id": "ma"},
            {"title": "Hindi", "id": "hi"},
            {"title": "Tamil", "id": "ta"},
            {"title": "Telegu", "id": "te"},
            {"title": "Kannada", "id": "kn"},
            {"title": "Marathi", "id": "mr"},
        ]
        
        for button in buttons:
            if language != "en":
                button["title"] = translator.translate(button["title"], dest=language).text
        
        # send the message with the translated buttons
        dispatcher.utter_message(text=message, buttons=buttons)
        return []

class ActionPayrollandattMenu(Action):
    def name(self) -> Text:
        return "action_payroll"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        language = tracker.slots.get("language")
        print(f"language: {language}")  # Debug statement
        if language != "en":
            translator = Translator()
            message = translator.translate("Please select your preferred option:", dest=language).text
        else:
            message = "Please select your preferred option:"
        buttons = [
            {"title": "Payroll", "id": "Payroll"},
            {"title": "Attendance", "id": "Attendance"},
        ]
        for button in buttons:
            if language != "en":
                button["title"] = translator.translate(button["title"], dest=language).text
        dispatcher.utter_message(text=message, buttons=buttons)
        return []



class ActionThanks(Action):  
    def name(self) -> Text:
        return "action_thanks"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        reversed_events = list(reversed(tracker.events))
        print(reversed_events)
        j=0
        data=[]
        for i in range(0,len(reversed_events)):
            if reversed_events[i]["event"]=="user" and j<2:
                #print(reversed_events[i]["text"],"\n")
                data.append(reversed_events[i]["text"])
                j=j+1   
        print(data)
        dispatcher.utter_message(text="Thanks for your reply. We will connect you soon")    
        return []
    
class ActionPF(Action):
    def name(self) -> Text:
        return "action_pf"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        language = tracker.slots.get('language')
        if not language:
            language = 'en'
        translator = Translator()
        message = translator.translate('Can you tell me what kind of details you need from your PF?', dest=language).text
        dispatcher.utter_message(text=message)
        return []

class ActionPayroll(Action):
    def name(self) -> Text:
        return "action_pay"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        language = tracker.slots.get('language')
        if not language:
            language = 'en'
        translator = Translator()
        message = translator.translate("Can you tell me what kind of details you need from your payroll?", dest=language).text
        dispatcher.utter_message(text=message)
        return []

class ActionAttendance(Action):
    def name(self) -> Text:
        return "action_attendance"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        language = tracker.slots.get('language')
        if not language:
            language = 'en'
        translator = Translator()
        message = translator.translate("Can you tell me what is your employee id?", dest=language).text
        dispatcher.utter_message(text=message)
        return []

class ActionReimbursementMenu(Action):
    def name(self) -> Text:
        return "action_reimbursement_menu"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        language = tracker.slots.get("language")
        if language != "en":
            translator = Translator()
            message = translator.translate("Please select from the following options for your Reimbursement claim:", dest=language).text
        else:
            message = "Please select from the following options for your Reimbursement claim:"

        buttons = [
            {"title": "Travel allowance", "id": "TA"},
            {"title": "Driver's salary", "id": "DS"},
            {"title": "Petrol allowance", "id": "PA"}
        ]
        for button in buttons:
            if language != "en":
                button["title"] = translator.translate(button["title"], dest=language).text
        dispatcher.utter_message(text=message, buttons=buttons)
        return []


class ActionTravelAllowance(Action):
    def name(self) -> Text:
        return "action_travel_allowance"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the user's preferred language from the language slot
        language = tracker.slots.get("language")
        # Set the default response text in English
        response_text = "The amount will be credited to your account."
        # Translate the response text to the user's preferred language using Googletrans
        if language:
            translator = Translator()
            response_text = translator.translate(response_text, dest=language).text
        # Send the translated response text back to the user
        dispatcher.utter_message(text=response_text)
        return []



class ActionPetrolAllowance(Action):
    def name(self) -> Text:
        return "action_Petrol_allowance"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        language = tracker.get_slot("language")
        translator = Translator()
        if language:
            translation = translator.translate("could you please tell me the distance you traveled.", dest=language)
            message = translation.text
        else:
            message = "could you please tell me the distance you traveled."
        dispatcher.utter_message(text=message)
        return []


class ActionDriverSalary(Action):
    def name(self) -> Text:
        return "action_Driver_salary"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        language = tracker.get_slot("language")
        translator = Translator()
        if language:
            translation = translator.translate("the amount will be credicted to the driver account.", dest=language)
            message = translation.text
        else:
            message = "the amount will be credicted to the driver account."
        dispatcher.utter_message(text=message)
        return []

class ActionDefault(Action):
    def name(self) -> Text:
        return "action_default"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #print("Tracker.Event",tracker.events,"\n\n")
        dispatcher.utter_message(text="Please hold on our staff busy")    
        return []
    
 
    
class ActionExit(Action):
    def name(self) -> Text:
        return "action_goodbye"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        language = tracker.slots.get('language')
        if not language:
            language = 'en'
        translator = Translator()
        message = translator.translate(text="Thank you for contacting us. We will be glad to assist you in future as well.", dest=language).text
        dispatcher.utter_message(text=message)
        return []
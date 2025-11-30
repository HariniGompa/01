import os
import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import Restarted

# response = requests.post("http://your-ml-api/predict", json=data)



class ValidateLoanApplicationForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_loan_application_form"

    async def validate_age(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        try:
            age = int(slot_value)
            if age < 18:
                dispatcher.utter_message(text="You must be at least 18 years old to apply for a loan.")
                return {"age": None}
            return {"age": age}
        except Exception:
            dispatcher.utter_message(text="Please enter a valid age (numbers only).")
            return {"age": None}

    async def validate_annual_salary(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        try:
            # allow formats like "500000", "5 LPA", "50k"
            s = str(slot_value).lower().replace(",", "").strip()
            # basic conversion heuristics
            if "l" in s:
                s = s.replace("l", "").replace("pa", "")
                salary = float(s) * 100000
            elif "k" in s:
                s = s.replace("k", "")
                salary = float(s) * 1000
            else:
                salary = float(s)
            if salary < 5000:
                dispatcher.utter_message(text="The salary looks too low. Please confirm.")
                return {"annual_salary": None}
            return {"annual_salary": salary}
        except Exception:
            dispatcher.utter_message(text="Please enter your salary as a number (e.g. 500000 or 5LPA).")
            return {"annual_salary": None}

    async def validate_credit_utilization(
        self, slot_value, dispatcher, tracker, domain
    ) -> Dict[Text, Any]:
        try:
            val = float(str(slot_value).replace("%", "").strip())
            if val < 0 or val > 100:
                dispatcher.utter_message(text="Credit utilization must be between 0 and 100 percent.")
                return {"credit_utilization": None}
            return {"credit_utilization": val}
        except Exception:
            dispatcher.utter_message(text="Please give credit utilization as a percentage, e.g. 45 or 45%.")
            return {"credit_utilization": None}


class ActionSubmitLoanApplication(Action):
    def name(self) -> Text:
        return "action_submit_loan_application"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        # collect slot values
        slots = tracker.current_slot_values()
        # prepare payload
        payload = {k: v for k, v in slots.items()}
        # Endpoint for ML model - set via environment variable ML_API_URL
        ml_url = os.environ.get("ML_API_URL", "http://localhost:5001/predict")

        try:
            resp = requests.post(ml_url, json=payload, timeout=10)
            resp.raise_for_status()
            result = resp.json()
            # Expecting result to contain {'eligibility': 'eligible'/'not_eligible', 'score': 0.87, ...}
            eligibility = result.get("eligibility", "unknown")
            score = result.get("score")
            if eligibility == "eligible":
                text = "Good news — based on the information provided, you appear eligible for the loan."
                if score is not None:
                    text += f" (Confidence: {round(score*100)}%)"
            elif eligibility == "not_eligible":
                text = "Based on the information provided, you are currently not eligible for the loan."
                if score is not None:
                    text += f" (Confidence: {round(score*100)}%)"
            else:
                text = "Our model could not determine eligibility right now. Our team will review your application."
        except Exception as e:
            text = "Sorry — we couldn't reach the eligibility service. Your details have been saved and will be processed by our team."
            # log error in real app

        dispatcher.utter_message(text=text)
        dispatcher.utter_message(text="If you'd like, I can connect you to a human agent or start another check.")
        return []


class ActionRestart(Action):
    """Resets the tracker to its initial state.
    Utters the restart confirmation and sets a new session.
    """
    def name(self) -> Text:
        return "action_restart"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # Send restart confirmation message
        dispatcher.utter_message(response="utter_restarted")
        
        # Return a restart event to clear the tracker
        return [Restarted()]

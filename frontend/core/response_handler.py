import logging
from typing import Optional

logger = logging.getLogger(__name__)

class ResponseHandler:
    def __init__(self, intent_detector):
        self.intent_detector = intent_detector

    def get_response(self, user_input: str) -> str:
        """Version améliorée avec suggestions"""
        intent = self.intent_detector.detect_intent(user_input)
        return self.intent_detector.get_response_for_intent(intent)

    def _format_response(self, response: str, intent: str) -> str:
        """Formate la réponse finale"""
        if intent == "unknown":
            return response + "\n\n(Posez votre question différemment si besoin)"
        return response
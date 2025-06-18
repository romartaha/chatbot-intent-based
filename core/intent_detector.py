import json
from pathlib import Path
from typing import Dict, List
import logging
from services.llm_service import call_llm_for_intent

logger = logging.getLogger(__name__)

class IntentDetector:
    def __init__(self, config_path: str = "config/responses.json"):
        self.config_path = Path(config_path)
        self.intents = self._load_intents()
        self.intent_map = self._create_intent_map()
        logger.info(f"Chargé {len(self.intents)} intentions depuis {config_path}")

    def _load_intents(self) -> List[Dict]:
        """Charge les intentions depuis le fichier JSON"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get("intents", [])
        except Exception as e:
            logger.error(f"Erreur de chargement des intentions: {e}")
            raise

    def _create_intent_map(self) -> Dict[str, Dict]:
        """Crée un mapping pour accès rapide"""
        return {intent['name'].lower(): intent for intent in self.intents}

    def detect_intent(self, user_input: str) -> str:
        """Version optimisée"""
        if not user_input.strip():
            return "empty_input"
        
        try:
            detected = call_llm_for_intent(user_input)
            if detected in self.intent_map:
                return detected
        except Exception as e:
            logger.error(f"Erreur LLM: {e}")
        
        return "unknown"

    def get_response_for_intent(self, intent_name: str) -> str:
        """Récupère la réponse depuis le JSON"""
        intent = self.intent_map.get(intent_name.lower())
        if not intent:
            logger.warning(f"Intention inconnue: {intent_name}")
            return "Je n'ai pas compris votre demande. Pouvez-vous reformuler ?"
        return intent.get("response", "Je n'ai pas compris votre demande. Pouvez-vous reformuler ?")
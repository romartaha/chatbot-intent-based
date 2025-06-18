# services/llm_service.py
import httpx
import json
from pathlib import Path
from typing import List, Dict
from config.settings import LLM_SERVER_URL
import logging

logger = logging.getLogger(__name__)

INTENTS_CONFIG_PATH = Path(__file__).parent.parent / "config" / "responses.json"
OPTIMIZED_PROMPT_TEMPLATE = """
### Rôle :
Vous êtes un classificateur d'intentions expert. Analysez strictement la question et choisissez UNIQUEMENT parmi ces intentions :

{formatted_intents}

### Règles strictes :
- Répondez UNIQUEMENT par le NOM EXACT de l'intention (identique à la liste)
- Si incertain, répondez 'unknown'
- Jamais d'explications ou de texte supplémentaire

### Exemples valides :
Question: "Comment obtenir un devis ?"
Réponse: demande_prix

Question: "Le site ne marche pas"
Réponse: support_technique

### Question à analyser :
"{user_input}"

### Réponse (nom d'intention uniquement) :
"""

def load_intents() -> List[Dict]:
    """Charge les intentions avec cache simple"""
    try:
        with open(INTENTS_CONFIG_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get("intents", [])
    except Exception as e:
        logger.error(f"Erreur de chargement des intentions: {e}")
        raise

def _get_intents_cache() -> List[Dict]:
    """Cache mémoire pour éviter de recharger le fichier"""
    if not hasattr(_get_intents_cache, 'cached_intents'):
        _get_intents_cache.cached_intents = load_intents()
    return _get_intents_cache.cached_intents

def format_prompt(user_input: str) -> str:
    """Formate le prompt de manière optimisée"""
    intents = _get_intents_cache()
    formatted_intents = "\n".join(
        f"- {intent['name']} (ex: {', '.join(intent['examples'][:2])}...)"
        for intent in intents
    )
    
    return OPTIMIZED_PROMPT_TEMPLATE.format(
        formatted_intents=formatted_intents,
        user_input=user_input
    )

def call_llm_for_intent(user_input: str) -> str:
    """
    Version optimisée pour la détection d'intention
    
    Args:
        user_input: Texte de l'utilisateur à analyser
        
    Returns:
        Nom de l'intention détectée ou 'unknown'
    """
    intents = _get_intents_cache()
    if not intents:
        logger.error("Aucune intention disponible pour la classification")
        return "unknown"

    # Pré-validation des entrées
    if not user_input or not isinstance(user_input, str):
        return "unknown"

    prompt = format_prompt(user_input)
    
    payload = {
        "prompt": prompt,
        "max_tokens": 15,  # Réduit pour forcer une réponse courte
        "temperature": 0.3,  # Un peu plus flexible que 0
        "top_p": 0.9,
        "stop": ["\n", "###", "<|endoftext|>"],
        "echo": False
    }

    try:
        with httpx.Client(timeout=15.0) as client:  # Timeout réduit
            response = client.post(
                f"{LLM_SERVER_URL}/completion",
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
            )
            response.raise_for_status()
            
            data = response.json()
            raw_response = data.get("content", "").strip()
            
            # Nettoyage et validation de la réponse
            cleaned_response = raw_response.split()[-1]  # Prend le dernier mot au cas où
            valid_intents = {intent['name'] for intent in intents}
            
            if cleaned_response in valid_intents:
                logger.debug(f"Intention valide détectée: {cleaned_response}")
                return cleaned_response
                
            logger.debug(f"Intention inconnue ou invalide: {raw_response}")
            return "unknown"

    except httpx.TimeoutException:
        logger.warning("Timeout du serveur LLM")
    except httpx.RequestError as e:
        logger.error(f"Erreur de requête: {e}")
    except Exception as e:
        logger.error(f"Erreur inattendue: {e}")
        
    return "unknown"
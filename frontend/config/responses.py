# config/responses.py
from yaml import safe_load, YAMLError
from typing import Optional
from pathlib import Path

def get_response_by_intent(intent_name: str) -> str:
    """Retrieve the appropriate response for a given intent from a YAML file.
    
    Args:
        intent_name: The name of the intent to search for
        
    Returns:
        The matching response or a default fallback message
    """
    try:
        # Use pathlib for more reliable path resolution
        file_path = Path(__file__).parent / "responses.yaml"
        
        with open(file_path, "r", encoding='utf-8') as f:
            data = safe_load(f)  # Note: using the directly imported safe_load
        
        # Handle case where file is empty or malformed
        if not data or "intents" not in data:
            return default_fallback_response()
            
        for intent in data["intents"]:
            if intent.get("name") == intent_name:
                return intent.get("response", default_fallback_response())
                
    except FileNotFoundError:
        print(f"Error: Responses file not found at {file_path}")
    except YAMLError as e:  # Note: using the directly imported YAMLError
        print(f"Error parsing YAML file: {e}")
    
    return default_fallback_response()

def default_fallback_response() -> str:
    """Default response when no match is found"""
    return "Désolé, je n'ai pas compris votre demande. Pouvez-vous reformuler ?"
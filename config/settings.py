# config/settings.py

import os

# === Configuration du serveur LLM local (llama.cpp) ===
LLM_SERVER_URL = os.getenv("LLM_SERVER_URL", "http://localhost:8080")

CACHE_ENABLED = os.getenv("CACHE_ENABLED", "True").lower() in ("true", "1", "yes")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
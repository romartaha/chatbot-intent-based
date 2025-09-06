import streamlit as st
from core.intent_detector import IntentDetector
from core.response_handler import ResponseHandler
import logging
from PIL import Image

# Config logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration de la page avec thème noir et violet
st.set_page_config(
    page_title="Chatbot INWI",
    page_icon="📱",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Injection CSS personnalisé pour thème noir INWI
st.markdown(
    """
    <style>
    /* Couleurs officielles INWI : violet (#9C27B0) sur fond noir */
    :root {
        --primary: #9C27B0;
        --secondary: #D500F9;
        --background: #000000;
        --card: #1A1A1A;
        --text: #FFFFFF;
    }
    
    /* Application du thème noir */
    .stApp {
        background-color: var(--background);
        color: var(--text);
    }
    
    /* En-tête */
    header {
        background-color: var(--background) !important;
        border-bottom: 1px solid var(--primary) !important;
    }
    
    /* Titres */
    h1, h2, h3, h4, h5, h6 {
        color: var(--primary) !important;
    }
    
    /* Boutons */
    .stButton>button {
        background-color: var(--primary) !important;
        color: white !important;
        border: none;
    }
    
    .stButton>button:hover {
        background-color: var(--secondary) !important;
    }
    
    /* Zone de saisie */
    .stTextInput>div>div>input {
        background-color: var(--card) !important;
        color: var(--text) !important;
        border: 1px solid var(--primary) !important;
    }
    
    /* Messages du chatbot */
    [data-testid="stChatMessage"] {
        padding: 12px;
        border-radius: 15px;
        margin-bottom: 15px;
    }
    
    /* Message utilisateur */
    [data-testid="stChatMessage"]:has(> div > div > .st-emotion-cache-4oy321) {
        background-color: #2E2E2E;
        border: 1px solid #4A4A4A;
    }
    
    /* Message assistant */
    [data-testid="stChatMessage"]:has(> div > div > [data-testid="stImage"]) {
        background-color: var(--card);
        border: 1px solid var(--primary);
    }
    
    /* Spinner de chargement */
    .stSpinner > div {
        background-color: var(--primary) !important;
    }
    
    /* Texte */
    p, .stMarkdown, .stText {
        color: var(--text) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

@st.cache_resource
def init_components():
    intent_detector = IntentDetector()
    response_handler = ResponseHandler(intent_detector)
    return intent_detector, response_handler

intent_detector, response_handler = init_components()

# En-tête personnalisé avec logo
try:
    logo = Image.open("winbyinwi.jpg")
    st.image(logo, width=150)
except:
    logger.warning("Logo INWI non trouvé")
    st.title("🤖 INWI Assistant")

st.header("Assistant Virtuel INWI", divider='violet')

# Historique
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Bonjour ! Je suis votre assistant INWI. Comment puis-je vous aider aujourd'hui ?"}
    ]

# Affichage historique
for msg in st.session_state.messages:
    avatar = "📱" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])

# Interaction
if prompt := st.chat_input("Écrivez votre message ici..."):
    # Ajout message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.write(prompt)
    
    # Réponse
    with st.chat_message("assistant", avatar="📱"):
        with st.spinner("Recherche en cours..."):
            try:
                response = response_handler.get_response(prompt)
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_msg = "Désolé, une erreur s'est produite. Veuillez réessayer."
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                logger.exception("Erreur dans le chat principal")
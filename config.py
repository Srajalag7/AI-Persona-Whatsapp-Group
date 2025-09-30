# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# File Paths
DATA_DIR = "data"
CHARACTERS_FILE = f"{DATA_DIR}/characters.json"
GROUPS_FILE = f"{DATA_DIR}/groups.json"
MESSAGES_FILE = f"{DATA_DIR}/messages.json"

# UI Configuration
MESSAGE_BATCH_SIZE = 20
TYPING_DELAY = 1.5  # seconds
DEFAULT_AVATARS = {
    "cricketer": "🏏",
    "comedian": "🎭",
    "tech_ceo": "💻",
    "bollywood": "🎬",
    "politician": "🎤",
    "influencer": "📱",
    "chef": "👨‍🍳",
    "rapper": "🎤",
    "default": "👤"
}

# Personality Traits
PERSONALITY_TRAITS = {
    "humor": "How funny and witty",
    "aggression": "How confrontational",
    "sarcasm": "Level of sarcasm",
    "energy": "Activity level in chat",
    "roasting": "Tendency to roast others",
    "meme_knowledge": "Understanding of internet culture",
    "formality": "How formal vs casual",
    "regional_touch": "Use of regional language/slang"
}

# Conversation Triggers
CHAOS_TRIGGERS = [
    "goa plan",
    "rcb",
    "party",
    "trip",
    "ipl",
    "virat",
    "bitcoin",
    "startup"
]
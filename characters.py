# characters.py
from typing import Dict, List, Optional
from utils import generate_id, save_json, load_json, get_timestamp
from config import CHARACTERS_FILE, DEFAULT_AVATARS

class Character:
    def __init__(self, character_id: str, name: str, archetype: str, 
                 system_prompt: str, traits: Dict[str, float], 
                 catchphrases: List[str] = None, avatar: str = None):
        self.id = character_id
        self.name = name
        self.archetype = archetype
        self.system_prompt = system_prompt
        self.traits = traits
        self.catchphrases = catchphrases or []
        self.avatar = avatar or DEFAULT_AVATARS.get(archetype, DEFAULT_AVATARS["default"])
        self.created_at = get_timestamp()
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "archetype": self.archetype,
            "system_prompt": self.system_prompt,
            "traits": self.traits,
            "catchphrases": self.catchphrases,
            "avatar": self.avatar,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        char = cls(
            data["id"], data["name"], data["archetype"],
            data["system_prompt"], data["traits"],
            data.get("catchphrases", []), data.get("avatar")
        )
        char.created_at = data.get("created_at", get_timestamp())
        return char

class CharacterManager:
    def __init__(self):
        self.characters = self._load_characters()
        if not self.characters:
            self._create_default_characters()
    
    def _load_characters(self) -> Dict[str, Character]:
        data = load_json(CHARACTERS_FILE, {})
        return {cid: Character.from_dict(cdata) for cid, cdata in data.items()}
    
    def _save_characters(self):
        data = {cid: char.to_dict() for cid, char in self.characters.items()}
        save_json(CHARACTERS_FILE, data)
    
    def create_character(self, name: str, archetype: str, system_prompt: str,
                        traits: Dict[str, float], catchphrases: List[str] = None) -> Character:
        char_id = generate_id()
        character = Character(char_id, name, archetype, system_prompt, 
                            traits, catchphrases)
        self.characters[char_id] = character
        self._save_characters()
        return character
    
    def get_character(self, character_id: str) -> Optional[Character]:
        return self.characters.get(character_id)
    
    def get_all_characters(self) -> List[Character]:
        return list(self.characters.values())
    
    def update_character(self, character_id: str, **kwargs):
        if character_id in self.characters:
            char = self.characters[character_id]
            for key, value in kwargs.items():
                if hasattr(char, key):
                    setattr(char, key, value)
            # Update avatar if archetype changed
            if 'archetype' in kwargs:
                char.avatar = DEFAULT_AVATARS.get(kwargs['archetype'], DEFAULT_AVATARS["default"])
            self._save_characters()
    
    def delete_character(self, character_id: str):
        if character_id in self.characters:
            del self.characters[character_id]
            self._save_characters()
    
    def _create_default_characters(self):
        """Create some default characters"""
        defaults = [
            {
                "name": "Virat Bhai",
                "archetype": "cricketer",
                "system_prompt": """You are Virat Bhai, an aggressive and passionate cricketer. You're super competitive, 
                get triggered by RCB jokes, love fitness, and always talk about dedication and commitment. You use 
                'BC' occasionally, get angry quickly, but also deeply care about your bros. You defend RCB fiercely 
                and roast MI fans. Always end messages with motivation or aggression.""",
                "traits": {
                    "humor": 0.4,
                    "aggression": 0.9,
                    "sarcasm": 0.6,
                    "energy": 0.8,
                    "roasting": 0.7,
                    "meme_knowledge": 0.3,
                    "formality": 0.3,
                    "regional_touch": 0.5
                },
                "catchphrases": ["Ben Stokes!", "Intent hai boss", "Let's go!", "BC yaar"]
            },
            {
                "name": "Tanmay Bhau",
                "archetype": "comedian",
                "system_prompt": """You are Tanmay Bhau, a meme lord and comedian. You're always laughing, making jokes, 
                and know every meme reference. You roast everyone lovingly, especially when they try to be serious. 
                You use 'bhau', 'bhai', and Mumbai slang. You're obsessed with YouTube, content creation, and make 
                everything into a joke. React with 'HAHAHAHA' and '💀' often.""",
                "traits": {
                    "humor": 1.0,
                    "aggression": 0.2,
                    "sarcasm": 0.8,
                    "energy": 0.9,
                    "roasting": 0.9,
                    "meme_knowledge": 1.0,
                    "formality": 0.1,
                    "regional_touch": 0.7
                },
                "catchphrases": ["HAHAHAHA", "Bhau kya kar raha hai", "Dead 💀", "Content hai boss"]
            },
            {
                "name": "Elon Bhaiya", 
                "archetype": "tech_ceo",
                "system_prompt": """You are Elon Bhaiya, a tech billionaire who's quirky and genius. You randomly talk about 
                Mars, Tesla, and memes. You make wild predictions, use rocket emojis 🚀, and casually mention buying 
                companies. You're simultaneously serious about tech and completely unhinged on social media. Drop crypto 
                and AI references randomly. Sometimes tweet like you're high.""",
                "traits": {
                    "humor": 0.7,
                    "aggression": 0.4,
                    "sarcasm": 0.8,
                    "energy": 0.6,
                    "roasting": 0.6,
                    "meme_knowledge": 0.9,
                    "formality": 0.2,
                    "regional_touch": 0.1
                },
                "catchphrases": ["To the moon 🚀", "Simulation confirmed", "Doge to Mars", "420 funding secured"]
            },
            {
                "name": "Deepika Didi",
                "archetype": "bollywood",
                "system_prompt": """You are Deepika Didi, a Bollywood queen who's elegant but also surprisingly savage. 
                You gossip about the industry, drop subtle shade, and know all the tea. You use 'darling', 'baby', 
                and mix Hindi-English. You're obsessed with manifestation, yoga, and mental health but also love 
                parties and drama. React with ✨ and 💅 often.""",
                "traits": {
                    "humor": 0.6,
                    "aggression": 0.3,
                    "sarcasm": 0.7,
                    "energy": 0.5,
                    "roasting": 0.5,
                    "meme_knowledge": 0.4,
                    "formality": 0.6,
                    "regional_touch": 0.6
                },
                "catchphrases": ["Manifestation works darling ✨", "Tea ☕", "Mental health is important baby", "Okayyyy then 💅"]
            },
            {
                "name": "Amit Ji",
                "archetype": "politician",
                "system_prompt": """You are Amit Ji, a cunning politician who speaks in riddles and makes everything political. 
                You use 'mitron', drop random statistics, and somehow connect everything to elections or master strokes. 
                You're formal but throw savage one-liners. You love chai, claim credit for everything good, and blame 
                opposition for everything bad.""",
                "traits": {
                    "humor": 0.5,
                    "aggression": 0.6,
                    "sarcasm": 0.9,
                    "energy": 0.4,
                    "roasting": 0.8,
                    "meme_knowledge": 0.2,
                    "formality": 0.8,
                    "regional_touch": 0.8
                },
                "catchphrases": ["Mitron", "Master stroke hai", "Chronology samajhiye", "Chai pe charcha"]
            }
        ]
        
        for char_data in defaults:
            self.create_character(**char_data)
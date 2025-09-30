# llm_handler.py
import google.generativeai as genai
from typing import List, Dict, Optional
import random
import os
import logging
from config import GEMINI_API_KEY

class LLMHandler:
    def __init__(self):
        if GEMINI_API_KEY:
            genai.configure(api_key=GEMINI_API_KEY)
            os.environ["GRPC_VERBOSITY"] = "ERROR"
            os.environ["GLOG_minloglevel"] = "2"

            logging.getLogger("absl").setLevel(logging.ERROR)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        else:
            self.model = None
            print("Warning: No Gemini API key found. Using mock responses.")
    
    def generate_response(self, character, messages: List[Dict], 
                         group_context: str = "", trigger_word: str = None) -> str:
        """Generate a response from a character"""
        
        if not self.model:
            return self._generate_mock_response(character)
        
        # Build conversation context
        context = self._build_context(character, messages, group_context, trigger_word)
        
        try:
            print(f"🤖 Gemini API call for {character.name}...")
            response = self.model.generate_content(context)
            print(f"✅ Response: {response.text[:50]}...")
            return self._post_process_response(response.text, character)
        except Exception as e:
            print(f"❌ Gemini API Error: {e}")
            return self._generate_mock_response(character)
    
    def _build_context(self, character, messages: List[Dict], 
                       group_context: str, trigger_word: str) -> str:
        """Build the prompt context for the LLM"""
        
        # Character personality
        prompt = f"""You are {character.name} in a WhatsApp group chat. 
{character.system_prompt}

GROUP PURPOSE: {group_context if group_context else "Roasting chat"}

Your personality traits (0-1 scale):
- Humor: {character.traits.get('humor', 0.5)}
- Aggression: {character.traits.get('aggression', 0.5)}
- Sarcasm: {character.traits.get('sarcasm', 0.5)}
- Energy: {character.traits.get('energy', 0.5)}
- Roasting tendency: {character.traits.get('roasting', 0.5)}
- Meme knowledge: {character.traits.get('meme_knowledge', 0.5)}

Your catchphrases: {', '.join(character.catchphrases)}

Recent conversation:
"""
        
        # Add recent messages
        for msg in messages[-10:]:
            prompt += f"\n{msg['name']}: {msg['content']}"
        
        # Add trigger context
        if trigger_word:
            prompt += f"\n\n(Someone mentioned '{trigger_word}' - react accordingly!)"
        
        prompt += f"""

Now respond as {character.name}. Keep it short (1-3 sentences), natural, and in character. 
Use WhatsApp style - casual, with emojis if fitting. Don't be too formal.

CRITICAL RULES:
- ONLY respond if you have something relevant to say about the current topic
- Stay focused on the GROUP PURPOSE: {group_context if group_context else "Roasting chat"}
- Don't randomly change topics unless it's natural
- Don't repeat what others just said
- Don't say random things unrelated to the conversation
- If the conversation is about the group purpose, engage meaningfully
- If you don't have anything relevant to add, don't respond at all
- Use your personality traits to guide your response style
"""
        
        return prompt
    
    def _post_process_response(self, response: str, character) -> str:
        """Clean up and enhance the response"""
        
        # Trim to reasonable length
        response = response.strip()
        if len(response) > 200:
            sentences = response.split('.')
            response = '.'.join(sentences[:2]) + '.'
        
        # Random chance to add catchphrase
        if character.catchphrases and random.random() > 0.7:
            response += f" {random.choice(character.catchphrases)}"
        
        return response
    
    def _generate_mock_response(self, character) -> str:
        """Generate a mock response when API is not available"""
        mock_responses = {
            "cricketer": [
                "Arre yaar, focus on the game! 🏏",
                "BC this is not the energy we need!",
                "Champions play with intent, not excuses 💪"
            ],
            "comedian": [
                "HAHAHAHA bhai kya scene hai 😂",
                "Dead 💀 This group is content gold",
                "Bhau, meme ban gaya tu toh"
            ],
            "tech_ceo": [
                "This is why we need to go to Mars 🚀",
                "AI will solve this in 2 years",
                "Simulation confirmed bros"
            ],
            "bollywood": [
                "Darling, this drama is too much ✨",
                "Manifesting better vibes only 💅",
                "The tea is piping hot today ☕"
            ],
            "politician": [
                "Mitron, this is a master stroke",
                "Chronology samajhiye friends",
                "Opposition ki saazish hai ye"
            ]
        }
        
        responses = mock_responses.get(character.archetype, 
                                       ["Interesting point!", "Hmm, let me think", "Good one bro"])
        
        response = random.choice(responses)
        if character.catchphrases and random.random() > 0.6:
            response += f" {random.choice(character.catchphrases)}"
        
        return response
    
    def should_character_respond(self, character, last_speaker: str, 
                                 energy_level: float) -> bool:
        """Determine if a character should respond"""
        
        # Don't respond to yourself
        if character.name == last_speaker:
            return False
        
        # Energy level affects response probability
        base_prob = character.traits.get('energy', 0.5)
        
        # Adjust based on conversation energy
        adjusted_prob = base_prob * (0.5 + energy_level * 0.5)
        
        return random.random() < adjusted_prob
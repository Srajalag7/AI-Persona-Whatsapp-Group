# conversation.py
import random
import time
from typing import List, Optional
from characters import CharacterManager
from groups import GroupManager
from llm_handler import LLMHandler
from config import CHAOS_TRIGGERS, TYPING_DELAY
from utils import should_trigger_chaos, get_random_reaction

class ConversationEngine:
    def __init__(self, char_manager: CharacterManager, 
                 group_manager: GroupManager):
        self.char_manager = char_manager
        self.group_manager = group_manager
        self.llm_handler = LLMHandler()
        self.active_conversations = {}
    
    def start_conversation(self, group_id: str, initial_topic: str = None):
        """Start a conversation in a group"""
        
        group = self.group_manager.get_group(group_id)
        if not group or not group.members:
            return False
        
        # Set group as active
        self.group_manager.update_group_state(group_id, True, "chatting")
        self.active_conversations[group_id] = {
            "energy": 0.7,
            "topic": initial_topic or "general",
            "last_speaker": None,
            "message_count": 0
        }
        
        # Start with a random member if topic is given
        if initial_topic:
            starter = random.choice(group.members)
            character = self.char_manager.get_character(starter)
            if character:
                self._send_message(group_id, character, 
                                 f"Arre guys, {initial_topic}! Kya scene hai?")
        
        return True
    
    def stop_conversation(self, group_id: str):
        """Stop a conversation"""
        self.group_manager.update_group_state(group_id, False, "idle")
        if group_id in self.active_conversations:
            del self.active_conversations[group_id]
    
    def process_user_message(self, group_id: str, message: str):
        """Process a message from the user"""
        
        # Add user message
        self.group_manager.add_message(
            group_id, "user", "You", message, "user"
        )
        
        # Check for chaos triggers
        if should_trigger_chaos(message, CHAOS_TRIGGERS):
            self._trigger_chaos_mode(group_id, message)
        else:
            self._generate_responses(group_id, message)
    
    def _generate_responses(self, group_id: str, trigger_message: str = None):
        """Generate responses from group members"""
        
        group = self.group_manager.get_group(group_id)
        if not group or not group.is_active:
            return
        
        # Get conversation state
        conv_state = self.active_conversations.get(group_id, {
            "energy": 0.5,
            "last_speaker": None,
            "message_count": 0,
            "recent_responses": []
        })
        
        # Get recent messages for context
        messages = self.group_manager.get_messages(group_id, limit=15)
        message_context = [
            {"name": msg.character_name, "content": msg.content}
            for msg in messages
        ]
        
        # Determine who responds
        responders = self._select_responders(group, conv_state, trigger_message)
        
        # Generate responses
        for character_id in responders:
            character = self.char_manager.get_character(character_id)
            if not character:
                continue
            
            # Check if this character has responded recently to avoid repetition
            if character.name in conv_state.get("recent_responses", [])[-3:]:
                continue
            
            # Generate response with group context
            group_context = group.description if group.description else "Roasting chat"
            response = self.llm_handler.generate_response(
                character, 
                message_context,
                group_context,
                trigger_message
            )
            
            # Check for repetitive content
            if self._is_repetitive_response(response, messages):
                continue
            
            # Send message
            self._send_message(group_id, character, response)
            
            # Update state
            conv_state["last_speaker"] = character.name
            conv_state["message_count"] += 1
            conv_state["recent_responses"] = conv_state.get("recent_responses", [])[-4:] + [character.name]
            
            # Random reactions
            if random.random() > 0.7:
                self._add_reaction(group_id, messages[-1] if messages else None)
            
            # Small delay between messages
            time.sleep(random.uniform(0.5, TYPING_DELAY))
        
        self.active_conversations[group_id] = conv_state
    
    def _select_responders(self, group, conv_state, trigger_message) -> List[str]:
        """Select which characters should respond"""
        
        responders = []
        energy = conv_state.get("energy", 0.5)
        
        # If chaos triggered, multiple people respond
        if trigger_message and should_trigger_chaos(trigger_message, CHAOS_TRIGGERS):
            num_responders = random.randint(2, min(4, len(group.members)))
            responders = random.sample(group.members, num_responders)
        else:
            # Normal flow - 1-2 responders based on energy
            for member_id in group.members:
                character = self.char_manager.get_character(member_id)
                if character and self.llm_handler.should_character_respond(
                    character, conv_state.get("last_speaker"), energy
                ):
                    responders.append(member_id)
                    if len(responders) >= 2:
                        break
        
        # Ensure at least one responder
        if not responders and group.members:
            responders = [random.choice(group.members)]
        
        return responders
    
    def _trigger_chaos_mode(self, group_id: str, trigger: str):
        """Trigger chaos mode - everyone starts talking"""
        
        group = self.group_manager.get_group(group_id)
        if not group:
            return
        
        # Increase energy
        if group_id in self.active_conversations:
            self.active_conversations[group_id]["energy"] = 0.9
        
        # Multiple quick responses
        self._generate_responses(group_id, trigger)
    
    def _send_message(self, group_id: str, character, content: str):
        """Send a message from a character"""
        self.group_manager.add_message(
            group_id, character.id, character.name, content, "normal"
        )
    
    def _add_reaction(self, group_id: str, message):
        """Add a reaction to a message"""
        if message and random.random() > 0.5:
            message.reactions.append(get_random_reaction())
            self.group_manager._save_messages()
    
    def _is_repetitive_response(self, response: str, messages: List) -> bool:
        """Check if response is too similar to recent messages"""
        if not messages:
            return False
        
        response_lower = response.lower()
        
        # Check against last 5 messages
        for msg in messages[-5:]:
            if msg.content.lower() in response_lower or response_lower in msg.content.lower():
                return True
        
        # Check for repeated phrases
        words = response_lower.split()
        if len(words) > 3:
            # Check if more than 70% of words are repeated from recent messages
            recent_text = " ".join([msg.content.lower() for msg in messages[-3:]])
            repeated_words = sum(1 for word in words if word in recent_text)
            if repeated_words / len(words) > 0.7:
                return True
        
        return False
    
    def auto_conversation(self, group_id: str, duration: int = 30):
        """Run an automatic conversation for specified duration"""
        
        if not self.start_conversation(group_id):
            return
        
        start_time = time.time()
        topics = [
            "Goa trip plan karte hain",
            "IPL auction ka kya scene hai",
            "New startup idea guys", 
            "Party kab kar rahe hain",
            "Bitcoin ka kya lagta hai"
        ]
        
        # Initial topic
        self.process_user_message(group_id, random.choice(topics))
        
        while time.time() - start_time < duration:
            if not self.group_manager.get_group(group_id).is_active:
                break
            
            # Random chance for new topic
            if random.random() > 0.8:
                self.process_user_message(group_id, random.choice(topics))
            else:
                self._generate_responses(group_id)
            
            time.sleep(random.uniform(2, 5))
        
        self.stop_conversation(group_id)
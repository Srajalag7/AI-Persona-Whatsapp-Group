# groups.py
from typing import Dict, List, Optional
from utils import generate_id, save_json, load_json, get_timestamp
from config import GROUPS_FILE, MESSAGES_FILE

class Message:
    def __init__(self, message_id: str, group_id: str, character_id: str,
                 character_name: str, content: str, message_type: str = "normal"):
        self.id = message_id
        self.group_id = group_id
        self.character_id = character_id
        self.character_name = character_name
        self.content = content
        self.message_type = message_type
        self.timestamp = get_timestamp()
        self.reactions = []
    
    def to_dict(self):
        return {
            "id": self.id,
            "group_id": self.group_id,
            "character_id": self.character_id,
            "character_name": self.character_name,
            "content": self.content,
            "message_type": self.message_type,
            "timestamp": self.timestamp,
            "reactions": self.reactions
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        msg = cls(
            data["id"], data["group_id"], data["character_id"],
            data["character_name"], data["content"], data.get("message_type", "normal")
        )
        msg.timestamp = data.get("timestamp", get_timestamp())
        msg.reactions = data.get("reactions", [])
        return msg

class Group:
    def __init__(self, group_id: str, name: str, description: str = ""):
        self.id = group_id
        self.name = name
        self.description = description
        self.members = []  # List of character IDs
        self.created_at = get_timestamp()
        self.is_active = False
        self.conversation_state = "idle"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "members": self.members,
            "created_at": self.created_at,
            "is_active": self.is_active,
            "conversation_state": self.conversation_state
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        group = cls(data["id"], data["name"], data.get("description", ""))
        group.members = data.get("members", [])
        group.created_at = data.get("created_at", get_timestamp())
        group.is_active = data.get("is_active", False)
        group.conversation_state = data.get("conversation_state", "idle")
        return group

class GroupManager:
    def __init__(self):
        self.groups = self._load_groups()
        self.messages = self._load_messages()
    
    def _load_groups(self) -> Dict[str, Group]:
        data = load_json(GROUPS_FILE, {})
        return {gid: Group.from_dict(gdata) for gid, gdata in data.items()}
    
    def _load_messages(self) -> Dict[str, List[Message]]:
        data = load_json(MESSAGES_FILE, {})
        messages = {}
        for group_id, msg_list in data.items():
            messages[group_id] = [Message.from_dict(msg) for msg in msg_list]
        return messages
    
    def _save_groups(self):
        data = {gid: group.to_dict() for gid, group in self.groups.items()}
        save_json(GROUPS_FILE, data)
    
    def _save_messages(self):
        data = {}
        for group_id, msg_list in self.messages.items():
            data[group_id] = [msg.to_dict() for msg in msg_list]
        save_json(MESSAGES_FILE, data)
    
    def create_group(self, name: str, description: str = "") -> Group:
        group_id = generate_id()
        group = Group(group_id, name, description)
        self.groups[group_id] = group
        self.messages[group_id] = []
        self._save_groups()
        self._save_messages()
        return group
    
    def get_group(self, group_id: str) -> Optional[Group]:
        return self.groups.get(group_id)
    
    def get_all_groups(self) -> List[Group]:
        return list(self.groups.values())
    
    def add_member(self, group_id: str, character_id: str):
        if group_id in self.groups and character_id not in self.groups[group_id].members:
            self.groups[group_id].members.append(character_id)
            self._save_groups()
    
    def remove_member(self, group_id: str, character_id: str):
        if group_id in self.groups and character_id in self.groups[group_id].members:
            self.groups[group_id].members.remove(character_id)
            self._save_groups()
    
    def get_members(self, group_id: str) -> List[str]:
        if group_id in self.groups:
            return self.groups[group_id].members
        return []
    
    def add_message(self, group_id: str, character_id: str, character_name: str,
                   content: str, message_type: str = "normal") -> Message:
        if group_id not in self.messages:
            self.messages[group_id] = []
        
        msg_id = generate_id()
        message = Message(msg_id, group_id, character_id, character_name,
                         content, message_type)
        self.messages[group_id].append(message)
        self._save_messages()
        return message
    
    def get_messages(self, group_id: str, limit: int = 50) -> List[Message]:
        if group_id in self.messages:
            return self.messages[group_id][-limit:]
        return []
    
    def clear_messages(self, group_id: str):
        if group_id in self.messages:
            self.messages[group_id] = []
            self._save_messages()
    
    def update_group_state(self, group_id: str, is_active: bool, state: str = "idle"):
        if group_id in self.groups:
            self.groups[group_id].is_active = is_active
            self.groups[group_id].conversation_state = state
            self._save_groups()
    
    def update_group_description(self, group_id: str, description: str):
        if group_id in self.groups:
            self.groups[group_id].description = description
            self._save_groups()
    
    def delete_group(self, group_id: str):
        if group_id in self.groups:
            del self.groups[group_id]
            if group_id in self.messages:
                del self.messages[group_id]
            self._save_groups()
            self._save_messages()
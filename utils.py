# utils.py
import json
import os
import uuid
from datetime import datetime
from typing import Dict, List, Any

def ensure_data_directory():
    """Create data directory if it doesn't exist"""
    if not os.path.exists("data"):
        os.makedirs("data")
        
def generate_id():
    """Generate unique ID"""
    return str(uuid.uuid4())[:8]

def get_timestamp():
    """Get current timestamp"""
    return datetime.now().isoformat()

def save_json(filepath: str, data: Any):
    """Save data to JSON file"""
    ensure_data_directory()
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_json(filepath: str, default: Any = None):
    """Load data from JSON file"""
    ensure_data_directory()
    if not os.path.exists(filepath):
        return default if default is not None else {}
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return default if default is not None else {}

def format_time(timestamp: str) -> str:
    """Format timestamp for display"""
    try:
        dt = datetime.fromisoformat(timestamp)
        return dt.strftime("%I:%M %p")
    except:
        return "Now"

def get_random_reaction():
    """Get random reaction emoji"""
    import random
    reactions = ["😂", "🔥", "❤️", "👍", "😅", "🤣", "💀", "😭", "🙌", "💯"]
    return random.choice(reactions)

def should_trigger_chaos(message: str, triggers: List[str]) -> bool:
    """Check if message contains chaos triggers"""
    message_lower = message.lower()
    return any(trigger in message_lower for trigger in triggers)
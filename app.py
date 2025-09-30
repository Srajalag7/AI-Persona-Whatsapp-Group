# app.py
import streamlit as st
import time
from datetime import datetime
from characters import CharacterManager
from groups import GroupManager
from conversation import ConversationEngine
from config import PERSONALITY_TRAITS, DEFAULT_AVATARS
from utils import format_time, ensure_data_directory

# Initialize session state
if 'char_manager' not in st.session_state:
    ensure_data_directory()
    st.session_state.char_manager = CharacterManager()
    st.session_state.group_manager = GroupManager()
    st.session_state.conv_engine = ConversationEngine(
        st.session_state.char_manager,
        st.session_state.group_manager
    )
    st.session_state.current_group = None
    st.session_state.auto_chat_running = False

# Page config
st.set_page_config(
    page_title="Bakchod AI WhatsApp",
    page_icon="💬",
    layout="wide"
)

# Custom CSS for WhatsApp-like styling
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a1014 0%, #1a2332 100%);
        color: #ffffff;
    }
    
    .chat-container {
        background: url("data:image/svg+xml,%3Csvg width='100' height='100' xmlns='http://www.w3.org/2000/svg'%3E%3Cdefs%3E%3Cpattern id='a' patternUnits='userSpaceOnUse' width='100' height='100'%3E%3Crect width='100' height='100' fill='%23151f27'/%3E%3Cpath d='M0 10h100v1H0zM0 30h100v1H0zM0 50h100v1H0zM0 70h100v1H0zM0 90h100v1H0z' fill='%231f2936' fill-opacity='0.1'/%3E%3C/pattern%3E%3C/defs%3E%3Crect width='100%25' height='100%25' fill='url(%23a)'/%3E%3C/svg%3E");
        padding: 15px;
        border-radius: 15px;
        height: 500px;
        overflow-y: auto;
        border: 1px solid #2a3a4a;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    
    .message-bubble {
        padding: 10px 15px;
        margin: 6px 0;
        border-radius: 18px;
        max-width: 75%;
        word-wrap: break-word;
        position: relative;
        box-shadow: 0 1px 3px rgba(0,0,0,0.2);
    }
    
    .user-message {
        background: linear-gradient(135deg, #005c4b 0%, #008069 100%);
        color: white;
        margin-left: auto;
        text-align: right;
        border-bottom-right-radius: 5px;
    }
    
    .ai-message {
        background: linear-gradient(135deg, #202c33 0%, #2a3a4a 100%);
        color: white;
        border-bottom-left-radius: 5px;
    }
    
    .message-name {
        font-size: 11px;
        font-weight: 600;
        margin-bottom: 3px;
        opacity: 0.9;
    }
    
    .message-time {
        font-size: 9px;
        opacity: 0.6;
        margin-top: 3px;
        font-style: italic;
    }
    
    .group-header {
        background: linear-gradient(135deg, #202c33 0%, #2a3a4a 100%);
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 15px;
        color: white;
        border: 1px solid #3a4a5a;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    .group-header h3 {
        margin: 0 0 5px 0;
        color: #ffffff;
        font-size: 18px;
    }
    
    .group-header p {
        margin: 0;
        opacity: 0.8;
        font-size: 14px;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a2332 0%, #0a1014 100%);
        border-right: 1px solid #2a3a4a;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #008069 0%, #005c4b 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #00a085 0%, #008069 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background-color: #2a3a4a;
        color: white;
        border: 1px solid #3a4a5a;
        border-radius: 8px;
    }
    
    .stTextArea > div > div > textarea {
        background-color: #2a3a4a;
        color: white;
        border: 1px solid #3a4a5a;
        border-radius: 8px;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background-color: #2a3a4a;
        color: white;
        border: 1px solid #3a4a5a;
        border-radius: 8px;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #008069 0%, #00a085 100%);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #2a3a4a 0%, #3a4a5a 100%);
        color: white;
        border-radius: 8px;
        border: 1px solid #4a5a6a;
    }
    
    .streamlit-expanderContent {
        background-color: #1a2332;
        border-radius: 0 0 8px 8px;
        border: 1px solid #4a5a6a;
        border-top: none;
    }
    
    /* Scrollbar styling */
    .chat-container::-webkit-scrollbar {
        width: 6px;
    }
    
    .chat-container::-webkit-scrollbar-track {
        background: #1a2332;
        border-radius: 3px;
    }
    
    .chat-container::-webkit-scrollbar-thumb {
        background: #4a5a6a;
        border-radius: 3px;
    }
    
    .chat-container::-webkit-scrollbar-thumb:hover {
        background: #5a6a7a;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("🔥 Bakchod AI WhatsApp Group 🔥")
    
    # Sidebar for controls
    with st.sidebar:
        st.header("⚙️ Controls")
        
        # Tab selection
        tab = st.radio("Select Mode", ["💬 Chat", "👥 Characters", "📱 Groups"])
        
        if tab == "💬 Chat":
            show_chat_controls()
        elif tab == "👥 Characters":
            show_character_management()
        elif tab == "📱 Groups":
            show_group_management()
    
    # Main chat area
    if tab == "💬 Chat" and st.session_state.current_group:
        show_chat_interface()
    elif tab == "💬 Chat":
        st.info("👈 Create a group and add members to start chatting!")
    elif tab == "👥 Characters":
        st.info("Manage AI characters from the sidebar")
    elif tab == "📱 Groups":
        st.info("Manage groups from the sidebar")

def show_chat_controls():
    """Show chat controls in sidebar"""
    
    st.subheader("📱 Select Group")
    
    groups = st.session_state.group_manager.get_all_groups()
    if groups:
        group_names = {g.name: g.id for g in groups}
        selected_group_name = st.selectbox(
            "Active Group",
            options=list(group_names.keys()),
            index=0 if not st.session_state.current_group else None
        )
        
        if selected_group_name:
            st.session_state.current_group = group_names[selected_group_name]
            group = st.session_state.group_manager.get_group(st.session_state.current_group)
            
            # Show group info
            st.write(f"**Description:** {group.description or 'No description'}")
            st.write(f"**Members:** {len(group.members)}")
            
            # Edit description
            with st.expander("✏️ Edit Group Description"):
                new_description = st.text_area("Group Description", 
                    value=group.description or "",
                    placeholder="What's this group about? (This context helps AI understand the vibe)")
                if st.button("Update Description"):
                    st.session_state.group_manager.update_group_description(group.id, new_description)
                    st.success("Description updated!")
                    st.rerun()
            
            # Show members
            if group.members:
                st.write("**Group Members:**")
                for member_id in group.members:
                    char = st.session_state.char_manager.get_character(member_id)
                    if char:
                        st.write(f"{char.avatar} {char.name}")
        
        # Conversation controls
        st.divider()
        st.subheader("🎮 Conversation Controls")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚀 Start Auto Chat", disabled=st.session_state.auto_chat_running):
                if st.session_state.current_group:
                    group = st.session_state.group_manager.get_group(st.session_state.current_group)
                    if group and group.members:
                        st.session_state.auto_chat_running = True
                        st.session_state.conv_engine.start_conversation(st.session_state.current_group, 
                                                                       "Yaar kuch interesting batao")
                        st.rerun()
        
        with col2:
            if st.button("⏹️ Stop Chat", disabled=not st.session_state.auto_chat_running):
                if st.session_state.current_group:
                    st.session_state.auto_chat_running = False
                    st.session_state.conv_engine.stop_conversation(st.session_state.current_group)
                    st.rerun()
        
        # Topic triggers
        st.write("**Quick Topics:**")
        topics = ["🏖️ Goa Trip", "🏏 IPL Auction", "🚀 Startup Ideas", 
                 "🎉 Party Plan", "💰 Crypto Talk"]
        
        for topic in topics:
            if st.button(topic):
                if st.session_state.current_group:
                    st.session_state.conv_engine.process_user_message(
                        st.session_state.current_group, 
                        topic.split(" ", 1)[1]
                    )
                    st.rerun()
        
        # Clear chat
        if st.button("🗑️ Clear Chat"):
            if st.session_state.current_group:
                st.session_state.group_manager.clear_messages(st.session_state.current_group)
                st.rerun()
    else:
        st.warning("No groups created yet! Go to Groups tab to create one.")

def show_character_management():
    """Show character management interface"""
    
    st.subheader("👥 Character Management")
    
    # Create new character
    with st.expander("➕ Create New Character", expanded=True):
        col1, col2 = st.columns([1, 1])
        
        with col1:
            name = st.text_input("Character Name", placeholder="e.g., Rohit Bhai")
            
            archetype = st.selectbox("Archetype", 
                ["cricketer", "comedian", "tech_ceo", "bollywood", 
                 "politician", "influencer", "chef", "rapper"])
            
            catchphrases = st.text_input("Catchphrases (comma-separated)", 
                placeholder="e.g., Let's go!, BC yaar, Bhau")
        
        with col2:
            st.write("**Preview:**")
            avatar = DEFAULT_AVATARS.get(archetype, DEFAULT_AVATARS["default"])
            st.write(f"{avatar} **{name or 'Character Name'}**")
            st.write(f"*{archetype.replace('_', ' ').title()}*")
        
        system_prompt = st.text_area("System Prompt", 
            placeholder="Describe the character's personality, speaking style, quirks, background, interests, how they interact with others...",
            height=120,
            help="Be detailed! The more you write, the better the AI will understand the character's personality.")
        
        st.write("**🎭 Personality Traits** (0 = Low, 1 = High)")
        
        # Group traits by category
        trait_categories = {
            "Social": ["humor", "energy", "roasting"],
            "Communication": ["sarcasm", "formality", "regional_touch"],
            "Behavior": ["aggression", "meme_knowledge"]
        }
        
        traits = {}
        for category, trait_keys in trait_categories.items():
            st.write(f"**{category}:**")
            cols = st.columns(len(trait_keys))
            for i, trait_key in enumerate(trait_keys):
                with cols[i]:
                    traits[trait_key] = st.slider(
                        PERSONALITY_TRAITS[trait_key], 
                        0.0, 1.0, 0.5, 0.1,
                        key=f"trait_{trait_key}",
                        help=f"Adjust {PERSONALITY_TRAITS[trait_key].lower()}"
                    )
        
        # Character preview
        if name and system_prompt:
            st.divider()
            st.write("**Character Preview:**")
            preview_col1, preview_col2 = st.columns([2, 1])
            
            with preview_col1:
                st.write(f"**{name}** - {archetype.replace('_', ' ').title()}")
                st.write(f"*{system_prompt[:100]}...*")
            
            with preview_col2:
                st.write("**Traits:**")
                for trait, value in traits.items():
                    st.progress(value, text=f"{PERSONALITY_TRAITS[trait]}: {value:.1f}")
        
        if st.button("✨ Create Character", type="primary"):
            if name and system_prompt:
                catchphrase_list = [c.strip() for c in catchphrases.split(",") if c.strip()]
                st.session_state.char_manager.create_character(
                    name, archetype, system_prompt, traits, catchphrase_list
                )
                st.success(f"🎉 Created {name}! They're ready to join groups.")
                st.rerun()
            else:
                st.error("Please fill in name and system prompt!")
    
    # List existing characters
    st.divider()
    st.write("**Existing Characters:**")
    
    characters = st.session_state.char_manager.get_all_characters()
    for char in characters:
        with st.expander(f"{char.avatar} {char.name} ({char.archetype})"):
            st.write(f"**System Prompt:** {char.system_prompt}")
            st.write(f"**Catchphrases:** {', '.join(char.catchphrases)}")
            st.write("**Traits:**")
            for trait, value in char.traits.items():
                st.progress(value, text=f"{PERSONALITY_TRAITS.get(trait, trait)}: {value:.1f}")
            
            # Edit character
            with st.expander(f"✏️ Edit {char.name}"):
                new_name = st.text_input("Name", value=char.name, key=f"edit_name_{char.id}")
                new_archetype = st.selectbox("Archetype", 
                    ["cricketer", "comedian", "tech_ceo", "bollywood", 
                     "politician", "influencer", "chef", "rapper"],
                    index=["cricketer", "comedian", "tech_ceo", "bollywood", 
                           "politician", "influencer", "chef", "rapper"].index(char.archetype),
                    key=f"edit_archetype_{char.id}")
                new_system_prompt = st.text_area("System Prompt", 
                    value=char.system_prompt, height=100, key=f"edit_prompt_{char.id}")
                
                st.write("**Personality Traits**")
                new_traits = {}
                cols = st.columns(2)
                for i, (trait_key, trait_desc) in enumerate(PERSONALITY_TRAITS.items()):
                    with cols[i % 2]:
                        new_traits[trait_key] = st.slider(trait_desc, 0.0, 1.0, 
                            char.traits.get(trait_key, 0.5), 0.1,
                            key=f"edit_trait_{trait_key}_{char.id}")
                
                new_catchphrases = st.text_input("Catchphrases (comma-separated)", 
                    value=', '.join(char.catchphrases), key=f"edit_catchphrases_{char.id}")
                
                if st.button(f"Update {char.name}", key=f"update_{char.id}"):
                    catchphrase_list = [c.strip() for c in new_catchphrases.split(",") if c.strip()]
                    st.session_state.char_manager.update_character(
                        char.id, name=new_name, archetype=new_archetype,
                        system_prompt=new_system_prompt, traits=new_traits,
                        catchphrases=catchphrase_list
                    )
                    st.success(f"Updated {new_name}!")
                    st.rerun()
            
            if st.button(f"Delete {char.name}", key=f"del_{char.id}"):
                st.session_state.char_manager.delete_character(char.id)
                st.rerun()

def show_group_management():
    """Show group management interface"""
    
    st.subheader("📱 Group Management")
    
    # Create new group
    with st.expander("➕ Create New Group"):
        group_name = st.text_input("Group Name", placeholder="e.g., Bakchod United")
        description = st.text_area("Group Description", 
            placeholder="What's this group about? (This context helps AI understand the vibe)")
        
        characters = st.session_state.char_manager.get_all_characters()
        char_options = {f"{c.avatar} {c.name}": c.id for c in characters}
        
        selected_chars = st.multiselect("Select Members", list(char_options.keys()))
        
        if st.button("Create Group"):
            if group_name and selected_chars:
                group = st.session_state.group_manager.create_group(group_name, description)
                for char_name in selected_chars:
                    st.session_state.group_manager.add_member(group.id, char_options[char_name])
                st.success(f"Created group: {group_name}")
                st.rerun()
    
    # List existing groups
    st.divider()
    st.write("**Existing Groups:**")
    
    groups = st.session_state.group_manager.get_all_groups()
    for group in groups:
        with st.expander(f"💬 {group.name}"):
            st.write(f"**Description:** {group.description or 'No description'}")
            st.write(f"**Created:** {group.created_at[:10]}")
            st.write(f"**Status:** {'🟢 Active' if group.is_active else '⚫ Idle'}")
            
            st.write("**Members:**")
            for member_id in group.members:
                char = st.session_state.char_manager.get_character(member_id)
                if char:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"{char.avatar} {char.name}")
                    with col2:
                        if st.button("Remove", key=f"rm_{group.id}_{member_id}"):
                            st.session_state.group_manager.remove_member(group.id, member_id)
                            st.rerun()
            
            # Add new member
            st.write("**Add Member:**")
            available_chars = [c for c in characters if c.id not in group.members]
            if available_chars:
                add_options = {f"{c.avatar} {c.name}": c.id for c in available_chars}
                new_member = st.selectbox(f"Add to {group.name}", 
                                         list(add_options.keys()),
                                         key=f"add_{group.id}")
                if st.button("Add", key=f"addbtn_{group.id}"):
                    st.session_state.group_manager.add_member(group.id, add_options[new_member])
                    st.rerun()
            
            # Delete group
            if st.button(f"🗑️ Delete Group", key=f"delgrp_{group.id}"):
                st.session_state.group_manager.delete_group(group.id)
                if st.session_state.current_group == group.id:
                    st.session_state.current_group = None
                st.rerun()

def show_chat_interface():
    """Show the main chat interface"""
    
    group = st.session_state.group_manager.get_group(st.session_state.current_group)
    if not group:
        st.error("Group not found!")
        return
    
    # Group header
    st.markdown(f"""
    <div class="group-header">
        <h3>{group.name}</h3>
        <p>{', '.join([st.session_state.char_manager.get_character(m).name 
                       for m in group.members 
                       if st.session_state.char_manager.get_character(m)][:3])}
           {f'+ {len(group.members)-3} more' if len(group.members) > 3 else ''}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Messages container
    messages_container = st.container()
    
    # Display messages
    messages = st.session_state.group_manager.get_messages(st.session_state.current_group)
    
    with messages_container:
        # Render each message individually
        for msg in messages:
            is_user = msg.message_type == "user"
            bubble_class = "user-message" if is_user else "ai-message"
            
            # Get character avatar
            avatar = "👤"
            if not is_user and msg.character_id:
                char = st.session_state.char_manager.get_character(msg.character_id)
                if char:
                    avatar = char.avatar
            
            # Render message bubble
            message_html = f"""
            <div class="message-bubble {bubble_class}">
                <div class="message-name">{avatar} {msg.character_name}</div>
                <div>{msg.content}</div>
                <div class="message-time">{format_time(msg.timestamp)}</div>
                {''.join(msg.reactions) if msg.reactions else ''}
            </div>
            """
            st.markdown(message_html, unsafe_allow_html=True)
    
    # User input
    st.divider()

    # Create inline layout using container
    input_container = st.container()
    with input_container:
        col1, col2 = st.columns([6, 1])

        with col1:
            user_input = st.text_input("message", key="user_message",
                                      placeholder="Join the chaos...", label_visibility="collapsed")

        with col2:
            send_clicked = st.button("Send 📤")

        if send_clicked and user_input:
            st.session_state.conv_engine.process_user_message(
                st.session_state.current_group, user_input
            )
            st.rerun()
    
    # Auto-refresh for active conversations
    if group.is_active and st.session_state.auto_chat_running:
        time.sleep(2)
        st.session_state.conv_engine._generate_responses(st.session_state.current_group)
        st.rerun()

if __name__ == "__main__":
    main()
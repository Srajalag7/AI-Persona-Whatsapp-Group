# 🔥 Bakchod AI WhatsApp Group 🔥

A chaotic, hilarious WhatsApp-style group chat where AI celebrities banter, roast each other, and create absolute chaos! Watch as Virat Bhai gets triggered by RCB jokes, Tanmay Bhau turns everything into memes, and Elon Bhaiya randomly mentions Mars while planning a Goa trip.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd bakchod-whatsapp-group
   ```

2. **Create virtual environment** (Recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```bash
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
   
   **Note**: Without an API key, the app will use mock responses which are still fun but less dynamic.

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:8501`

## 🎮 How to Use

### 1. Create Characters
- Go to the **👥 Characters** tab
- Click **➕ Create New Character**
- Fill in character details:
  - **Name**: e.g., "Rohit Bhai", "Deepika Didi"
  - **Archetype**: Choose from cricketer, comedian, tech_ceo, etc.
  - **System Prompt**: Detailed personality description
  - **Personality Traits**: Adjust sliders for humor, aggression, energy, etc.
  - **Catchphrases**: Add signature phrases

### 2. Create Groups
- Go to the **📱 Groups** tab
- Click **➕ Create New Group**
- Add a group name and description
- Select characters to join the group
- The description helps AI understand the group's vibe

### 3. Start Chatting
- Go to the **💬 Chat** tab
- Select your group from the dropdown
- Click **🚀 Start Auto Chat** to begin the chaos
- Use **Quick Topics** buttons to trigger specific conversations
- Type your own messages to join the conversation
- Click **⏹️ Stop Chat** when you've had enough chaos

## 📁 Project Structure

```
bakchod-whatsapp-group/
├── app.py                 # Main Streamlit application
├── characters.py          # Character management system
├── groups.py              # Group and message management
├── conversation.py        # Conversation engine
├── llm_handler.py         # LLM integration (Gemini)
├── config.py              # Configuration and constants
├── utils.py               # Utility functions
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── data/                  # JSON data storage
    ├── characters.json    # Character data
    ├── groups.json        # Group data
    └── messages.json      # Message history
```

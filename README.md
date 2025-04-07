# AI Companion - Backend System

## Overview

This project implements the backend system for an AI Companion designed for real-time voice conversations. It focuses on understanding the user's emotional state during the conversation, generating insights, and using this knowledge to personalize future interactions, all operating silently in the background.

The system captures conversations, analyzes transcripts for emotional cues and topics using both basic sentiment analysis and advanced LLM analysis (via Groq/Llama 3), generates user profiles, uploads these profiles to a knowledge base (ElevenLabs Conversational AI), and tracks mood evolution over time.

## Features Implemented (Backend)

*   **Real-time Voice Conversation:** Utilizes ElevenLabs Conversational AI for voice interaction.
*   **Basic Emotion Detection:** Uses `TextBlob` for immediate sentiment analysis (positive, neutral, negative) during the conversation.
*   **Escalation Detection:** Simple keyword spotting for high-risk terms.
*   **Coping Strategies:** Provides basic coping advice based on detected sentiment.
*   **Transcript Saving:** Automatically saves conversation transcripts to the `/conversations` directory.
*   **Advanced LLM Analysis:** Uses Groq API (Llama 3 70b) to analyze transcripts for deeper insights:
    *   User Name Inference
    *   Dominant Mood
    *   Emotion Trend
    *   Key Topics Discussed
    *   Descriptive Profile Tags
    *   Concise Persona Summary
*   **User Profile Generation:** Saves the LLM analysis results as structured JSON files in `/user_profiles`.
*   **Knowledge Base Integration:** Formats the user profile into text and uploads it to the ElevenLabs Conversational AI knowledge base API, enabling the agent to leverage this information in subsequent conversations.
*   **Automated Workflow:** The process of transcript saving, analysis, profile generation, and knowledge base upload is automatically triggered after each conversation ends.
*   **Mood Evolution Tracking:** Analyzes profiles over time to calculate mood scores, generate insights (e.g., "You seem more positive than last time"), detect potential emotional degradation trends, and create a mood graph.
*   **Mood API Endpoint:** Provides a Flask endpoint (`/mood-trends`) to view mood insights, scores, and the generated mood graph (`mood_evolution.png`).

## Project Structure

```
/
|-- conversations/          # Saved conversation transcripts (.txt)
|-- user_profiles/          # Generated user profiles (.json)
|-- src/                    # Source code directory
|   |-- __init__.py         # Makes src a Python package
|   |-- agent.py            # Main script: Runs the conversation, triggers post-processing
|   |-- emotion_analysis.py # Basic sentiment analysis (TextBlob) & escalation check
|   |-- coping_strategies.py# Provides advice based on basic sentiment
|   |-- analyzer_agent.py   # LLM analysis using Groq API, saves JSON profiles
|   |-- knowledge_uploader.py# Formats profiles & uploads them to ElevenLabs KB
|   |-- mood_tracker.py     # Analyzes historical profiles, provides API endpoint, generates graph
|   |-- scheduler.py        # (Optional) Alternative script for scheduled analysis/uploads
|   |-- sync_user_profile.py# (Optional) Alternative script for scheduled KB sync
|   |-- watcher_processor.py# (NEW) A separate, long-running script that periodically checks the ElevenLabs API for new conversations
|   |-- demo_full_loop.py   # (REVISED) A script specifically for demonstrating the *live* conversation part
|   |-- processed_conversation_ids.txt# (NEW) Automatically created by watcher_processor.py to store the IDs of conversations that have already been processed, preventing duplicates
|-- .env                    # Environment variables (API keys, Agent ID)
|-- requirements.txt        # Python dependencies
|-- README.md               # This file
|-- mood_evolution.png      # Generated mood graph (created by mood_tracker.py in project root)
```

## File Descriptions

*   **`src/agent.py`**: The main entry point. Initializes and runs the ElevenLabs conversation. After the session ends, it retrieves the transcript, saves it, then calls functions from `analyzer_agent.py` and `knowledge_uploader.py`.
*   **`src/emotion_analysis.py`**: Contains functions using `TextBlob` to get basic sentiment and check for specific escalation keywords.
*   **`src/coping_strategies.py`**: Provides simple, pre-defined coping advice.
*   **`src/analyzer_agent.py`**: Contains functions to analyze transcript using Groq API and save the profile JSON to `user_profiles/`.
*   **`src/knowledge_uploader.py`**: Contains functions to format a profile JSON and upload it to the ElevenLabs knowledge base.
*   **`src/mood_tracker.py`**: Flask app to analyze profiles in `user_profiles/`, generate `mood_evolution.png` (in the project root), and serve insights at `/mood-trends`.
*   **`watcher_processor.py`**: (NEW) A separate, long-running script that periodically checks the ElevenLabs API for new conversations. When it finds one that hasn't been processed, it fetches the transcript, saves it, triggers the analysis (`src/analyzer_agent.py`), saves the profile, and uploads the profile to the KB (`src/knowledge_uploader.py`). It keeps track of processed IDs in `processed_conversation_ids.txt`.
*   **`demo_full_loop.py`**: (REVISED) A script specifically for demonstrating the *live* conversation part. It runs the voice chat and shows real-time analysis, but **does not** handle post-conversation processing itself. It relies on `watcher_processor.py` for that.
*   **`processed_conversation_ids.txt`**: (NEW) Automatically created by `watcher_processor.py` to store the IDs of conversations that have already been processed, preventing duplicates.
*   **`.env`**: Stores sensitive API keys and configuration.
*   **`requirements.txt`**: Lists all necessary Python packages.

## Workflow (Decoupled)

1.  **Run the Watcher:** Start `python watcher_processor.py` in a terminal. It runs continuously in the background, checking for new conversations every minute (configurable).
2.  **Run the Live Conversation:** Start `python demo_full_loop.py` (or `python src/agent.py`) in another terminal.
3.  Engage in a voice conversation.
4.  End the conversation (Ctrl+C). The demo/agent script finishes (it might show an `OSError` which is okay).
5.  **Watcher Takes Over:** Within the next minute (or configured interval), `watcher_processor.py` will:
    *   Detect the newly completed conversation via the API.
    *   Fetch and save the transcript to `conversations/`.
    *   Call the analysis function, saving a profile to `user_profiles/`.
    *   Call the upload function, sending the profile to ElevenLabs KB.
    *   Log the conversation ID to `processed_conversation_ids.txt`.
6.  (Separately) Run `python src/mood_tracker.py` to start the Flask server for historical mood data, which reads from `user_profiles/`.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd <repository-directory>
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
   pip install -r requirements.txt
   ```
4.  **Create `.env` file:** Create a file named `.env` in the project root and add your API keys and Agent ID:
    ```dotenv
    AGENT_ID=your_elevenlabs_agent_id
    ELEVENLABS_API_KEY=your_elevenlabs_api_key
    GROQ_API_KEY=your_groq_api_key
    ```
    Replace the placeholder values with your actual credentials.

## Running the System (Decoupled)

**Important:** Run commands from the project root directory.

1.  **Start the Watcher/Processor:**
    Open a terminal and run:
    ```bash
    python watcher_processor.py
    ```
    Keep this script running in the background. It will automatically process conversations after they end.

2.  **Start the Mood Tracker (Optional):**
    Open another terminal and run:
    ```bash
    python src/mood_tracker.py
    ```
    Keep this running to access historical mood data via `http://localhost:5000/mood-trends`.

3.  **Run the Live Conversation Demo:**
    Open a *third* terminal and run:
    ```bash
    python demo_full_loop.py
    ```
    Have the conversation. Press `Ctrl+C` to end. The post-processing will be handled automatically by the watcher script running in the first terminal.
    *(Alternatively, run `python src/agent.py` for the less verbose version).* 
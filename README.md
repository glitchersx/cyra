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
|-- .env                    # Environment variables (API keys, Agent ID)
|-- agent.py                # Main script: Runs the conversation, triggers post-processing
|-- emotion_analysis.py     # Basic sentiment analysis (TextBlob) & escalation check
|-- coping_strategies.py    # Provides advice based on basic sentiment
|-- conversation_manager.py # (Deprecated/Integrated) Original transcript saving logic
|-- analyzer_agent.py       # LLM analysis using Groq API, saves JSON profiles
|-- knowledge_uploader.py   # Formats profiles & uploads them to ElevenLabs KB
|-- mood_tracker.py         # Analyzes historical profiles, provides API endpoint, generates graph
|-- scheduler.py            # (Optional) Alternative script for scheduled analysis/uploads
|-- sync_user_profile.py    # (Optional) Alternative script for scheduled KB sync
|-- requirements.txt        # Python dependencies
|-- README.md               # This file
|-- mood_evolution.png      # Generated mood graph (created by mood_tracker.py)
```

## File Descriptions

*   **`agent.py`**: The main entry point. Initializes and runs the ElevenLabs conversation. After the session ends, it retrieves the transcript, saves it, then calls `analyzer_agent.py` to generate a profile and `knowledge_uploader.py` to upload the profile.
*   **`emotion_analysis.py`**: Contains functions using `TextBlob` to get basic sentiment and check for specific escalation keywords in user utterances during the live conversation.
*   **`coping_strategies.py`**: Provides simple, pre-defined coping advice mapped to the basic sentiments detected by `emotion_analysis.py`.
*   **`analyzer_agent.py`**: Takes a transcript file path, sends the content to the Groq API (Llama 3 70b model) with a specific prompt to extract structured user profile information (mood, topics, tags, summary), and saves this as a JSON file in `user_profiles/`.
*   **`knowledge_uploader.py`**: Takes a generated user profile JSON file path, reads it, formats the content into readable text, and uploads this text to the configured ElevenLabs Conversational AI knowledge base using their API.
*   **`mood_tracker.py`**: Loads all profiles from `user_profiles/`, calculates mood scores over time, generates comparative insights, flags potential degradation trends, creates a `mood_evolution.png` graph, and serves this information via a Flask API endpoint at `/mood-trends`.
*   **`.env`**: Stores sensitive API keys and configuration (Agent ID, ElevenLabs API Key, Groq API Key). **Never commit this file to Git.**
*   **`requirements.txt`**: Lists all necessary Python packages.

## Workflow

1.  Run `python agent.py`.
2.  Engage in a voice conversation with the ElevenLabs agent.
3.  During the conversation, basic emotion/escalation analysis is performed and printed to the console.
4.  End the conversation (Ctrl+C).
5.  `agent.py` automatically fetches and saves the transcript to `conversations/`.
6.  `agent.py` calls `analyzer_agent.py` to process the transcript:
    *   Groq/Llama 3 analyzes the text.
    *   A profile is saved to `user_profiles/`.
7.  `agent.py` calls `knowledge_uploader.py` to process the new profile:
    *   The profile JSON is formatted into text.
    *   The text is uploaded to the ElevenLabs knowledge base.
8.  (Separately) Run `python mood_tracker.py` to start the Flask server.
9.  Access `http://localhost:5000/mood-trends` in a browser to see historical mood analysis and the generated graph (`mood_evolution.png`).

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

## Running the System

1.  **Run the Mood Tracker (Optional, for historical analysis):**
    Open a terminal and run:
    ```bash
    python mood_tracker.py
    ```
    Keep this running. Access the data at `http://localhost:5000/mood-trends`.

2.  **Run the Main Conversation Agent:**
    Open another terminal and run:
    ```bash
    python agent.py
    ```
    Start speaking. Press `Ctrl+C` to end the session and trigger the post-conversation analysis and upload workflow. 

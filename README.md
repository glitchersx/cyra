# Your Personal AI Companion

Bring your own conversational AI assistant to life! This project lets you chat with your AI companion using your voice or text, and easily manage your past conversations.

It's a starting point for building applications with a voice AI you can talk to naturally.

## Features

*   **Real-time Voice Conversations:** Talk directly with your AI assistant.
*   **Web Interface:** A simple dashboard to view, save, and manage your conversation history.
*   **Conversation Management:** Tools to list, save, and delete past chats via command line or the web UI.
*   **(Optional) Text Chat:** A text-based interface for interacting with the AI.

## Setup

1.  **Python Environment:** Make sure you have Python installed. It's best to use a virtual environment:
    ```bash
    # Create the environment
    python -m venv venv
    # Activate it
    # Windows:
    .\venv\Scripts\activate
    # macOS/Linux:
    source venv/bin/activate
    ```

2.  **Install Dependencies:**
    *   Install the required Python libraries (including the core AI communication library):
        ```bash
        pip install -r requirements.txt
        ```
    *   Make sure you have Node.js and npm installed for the web frontend ([https://nodejs.org/](https://nodejs.org/)).
    *   Set up the frontend dependencies:
        ```bash
        python setup_frontend.py
        ```

## Usage

### 1. Configure Your AI

You need to tell the application how to connect to *your* specific AI agent. Set these environment variables:

*   `AGENT_ID` (or `AGENT1_ID`/`AGENT2_ID`): The unique identifier for your configured AI agent.
*   `ELEVENLABS_API_KEY` (or `ELEVENLABS_API_KEY1`/`ELEVENLABS_API_KEY2`): Your API key for the underlying AI service.

**How to Set Environment Variables:**

*   **(Recommended) `.env` file:** Create a file named `.env` in the project root and add your keys:
    ```
    AGENT1_ID="your_agent_1_id"
    ELEVENLABS_API_KEY1="your_api_key_1"
    # Add AGENT2_ID / ELEVENLABS_API_KEY2 if using agent2.py
    ```
    *(Ensure `.env` is in your `.gitignore`!)*
*   **(Temporary) PowerShell Example:**
    ```powershell
    $env:AGENT1_ID="your_agent_id"
    $env:ELEVENLABS_API_KEY1="your_api_key"
    ```

### 2. Start Talking! (Voice Demo)

Run the voice conversation script (make sure your environment variables are set):

```bash
# Example using agent1 configuration
python agent1.py
```

This will:

1.  Start a live voice conversation with your AI assistant.
2.  Listen via your microphone.
3.  Respond with the AI's voice through your speakers.
4.  Show the transcript in the console.
5.  End when you press `Ctrl+C`.

*(Use `agent2.py` if you have configured a second agent/key)*

### 3. Manage Your Conversations (Web Dashboard)

Get a visual overview of your chat history.

1.  **Start the Backend API:**
    (Ensure environment variables are set)
    ```bash
    python api.py
    ```

2.  **Start the Frontend:**
    (In a *separate* terminal)
    ```bash
    cd frontend
    npm start
    ```

3.  **Open the Dashboard:** Navigate to `http://localhost:3000` in your browser.

The web interface allows you to:

*   View all your past conversations.
*   See detailed transcripts.
*   Save transcripts to local files.
*   Delete conversations you no longer need.

### 4. Manage Conversations (Command Line)

You can also manage conversations directly from the terminal:

*   **Demo Script:** See examples of listing, viewing, and saving.
    ```bash
    python manage_conversations.py
    ```
*   **Full CLI Tool:**
    ```bash
    python conversation_manager.py [command] [options]
    ```
    *   **Commands:** `list`, `get [id]`, `save [id]`, `delete [id]`
    *   Get help: `python conversation_manager.py --help`

## How It Works (Simplified)

1.  The scripts use your unique Agent ID and API Key to connect to the AI service.
2.  A conversation session is established with your AI assistant.
3.  You interact through voice (using microphone/speakers) or text.
4.  The system keeps track of conversations using unique IDs.
5.  Management tools (web UI, CLI) allow you to interact with the stored conversation history. 
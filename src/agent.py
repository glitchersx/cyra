import os
import signal
import json
import time
from dotenv import load_dotenv # Import dotenv

# MODIFIED: Import the combined function
from emotion_analysis import get_emotion_and_check_escalation
from coping_strategies import get_coping_advice
# NEW: Import functions from other modules
from analyzer_agent import analyze_and_save_profile
from knowledge_uploader import upload_profile_file

from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface

load_dotenv() # Load .env file

# Load agent ID and API key from environment variables
# Ensure these match your .env file or environment setup
agent_id = os.getenv("AGENT_ID") # Using AGENT1_ID as default now
api_key = os.getenv("ELEVENLABS_API_KEY") # Changed back to standard key name

if not agent_id or not api_key:
    print("Error: AGENT1_ID and ELEVENLABS_API_KEY must be set in environment variables.")
    exit()

# Create the ElevenLabs client instance
client = ElevenLabs(api_key=api_key)

# NEW: Define a function to handle user transcript processing
def process_user_transcript(transcript: str):
    """
    Processes the user's transcript, performs emotion analysis, checks for
    escalation, and prints relevant information or advice.
    """
    print(f"User: {transcript}")

    # Get emotion and check for escalation flags
    emotion, escalation_needed = get_emotion_and_check_escalation(transcript)
    print(f"   [Detected Emotion: {emotion}]")

    # Handle escalation OR provide coping advice
    if escalation_needed:
        # IMPORTANT: This is a placeholder. Real applications need robust handling.
        print("*-* ESCALATION DETECTED *-*")
        print("   It sounds like you're going through a really tough time. Please know that help is available.")
        print("   Consider reaching out to a crisis hotline or mental health professional.")
        print("   [Placeholder: Link/Number to Crisis Support]") 
        # TODO: Trigger frontend popup/alert (Phase 5)
        # TODO: Potentially stop the conversation or change agent behavior here?
    else:
        # Get coping advice based on emotion if no escalation needed
        advice = get_coping_advice(emotion)
        print(f"   [Suggested Action/Reflection: {advice}]")

    # TODO: Future integration - maybe send advice back to agent to speak?
    # TODO: Future integration - update UI with emotion/advice

# Initialize the Conversation instance
conversation = Conversation(
    # API client and agent ID
    client,
    agent_id,

    # Assume auth is required when API_KEY is set
    requires_auth=bool(api_key),

    # Use the default audio interface
    audio_interface=DefaultAudioInterface(),

    # Simple callbacks that print the conversation to the console
    callback_agent_response=lambda response: print(f"Agent: {response}"),
    callback_agent_response_correction=lambda original, corrected: print(f"Agent: {original} -> {corrected}"),
    # MODIFIED: Use the new processing function for user transcript
    callback_user_transcript=process_user_transcript,

    # Uncomment if you want to see latency measurements
    # callback_latency_measurement=lambda latency: print(f"Latency: {latency}ms"),
)

# Start the conversation
print("Starting AI Companion session...")
print("Speak into your microphone. Press Ctrl+C to end.")

conversation_id = None
transcript_filepath = None

signal.signal(signal.SIGINT, lambda sig, frame: conversation.end_session())

recovered_id = False # Flag to indicate if we used the recovery method

try:
    conversation.start_session()
    print("Waiting for session to end...")
    conversation_id = conversation.wait_for_session_end()
    print(f"Session ended. Conversation ID: {conversation_id}")

except OSError as e:
    print(f"Caught OSError during session end: {e}")
    # Attempt direct attribute access first (might work sometimes)
    if hasattr(conversation, 'conversation_id') and conversation.conversation_id:
        conversation_id = conversation.conversation_id
        print(f"Retrieved Conversation ID via attribute after error: {conversation_id}")
    else:
        print("Could not retrieve Conversation ID directly after OSError.")
except Exception as e:
    print(f"Caught unexpected Exception during session end: {e}")
    import traceback
    traceback.print_exc()
    # Attempt direct attribute access first
    if hasattr(conversation, 'conversation_id') and conversation.conversation_id:
        conversation_id = conversation.conversation_id
        print(f"Retrieved Conversation ID via attribute after unexpected error: {conversation_id}")
    else:
        print("Could not retrieve Conversation ID directly after unexpected error.")

# --- NEW: Recovery Logic --- 
if not conversation_id:
    print("\n--- Attempting to recover latest conversation ID via API list... ---")
    try:
        # Fetch the single most recent conversation for this agent
        recent_conversations = client.conversational_ai.list_conversations(agent_id=agent_id, page_size=1)
        if recent_conversations and len(recent_conversations) > 0:
            latest_conv = recent_conversations[0]
            conversation_id = latest_conv.get('conversation_id')
            if conversation_id:
                print(f"--- Successfully recovered latest Conversation ID: {conversation_id} ---")
                recovered_id = True
            else:
                print("--- Found latest conversation, but it has no ID. ---")
        else:
            print("--- API returned no recent conversations for this agent. ---")
    except Exception as api_err:
        print(f"--- Error calling list_conversations API: {api_err} ---")
# --- End Recovery Logic ---

# --- Post-Conversation Processing --- 
if conversation_id:
    print("\n--- Starting Post-Conversation Processing --- ")
    if recovered_id:
        print("(Using recovered Conversation ID)")
    try:
        # 1. Get and Save Transcript
        print(f"Fetching details for conversation: {conversation_id}")
        # Increased sleep slightly just in case recovery method introduces timing issues
        time.sleep(3) 
        conv_data = client.conversational_ai.get_conversation(conversation_id)
        transcript = conv_data.get('transcript', None)

        if transcript:
            history = []
            for entry in transcript:
                role = "User" if entry.get('role') == 'user' else "Agent"
                message = entry.get('message', '[message missing]')
                history.append(f"{role}: {message}")

            conv_dir = "conversations"
            os.makedirs(conv_dir, exist_ok=True)
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            transcript_filename = f"conversation_{conversation_id}_{timestamp}.txt"
            transcript_filepath = os.path.join(conv_dir, transcript_filename)
            
            with open(transcript_filepath, 'w', encoding='utf-8') as f:
                f.write('\n'.join(history))
            print(f"--- Conversation successfully saved to {transcript_filepath} ---")
        else:
             print("Warning: Transcript not found or empty in API response. Skipping analysis and upload.")
             transcript_filepath = None # Ensure path is None if not saved

        # 2. Analyze Transcript and Save Profile (if transcript saved)
        profile_filepath = None
        if transcript_filepath:
            profile_filepath = analyze_and_save_profile(transcript_filepath)
        
        # 3. Upload Profile to Knowledge Base (if profile saved)
        if profile_filepath:
            upload_profile_file(profile_filepath)
        else:
            print("--- Skipping knowledge base upload as profile was not generated or transcript failed. ---")
            
    except Exception as e:
        import traceback
        print(f"--- Error during post-conversation processing: {str(e)} ---")
        print("Traceback:")
        traceback.print_exc()
    
    print("--- Post-Conversation Processing Finished --- ")

else:
    print("--- Skipping post-conversation processing: Could not obtain or recover Conversation ID. ---")

print("\nAI Companion session complete.") 
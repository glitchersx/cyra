import os
import signal
import json
import time

from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface

# Load agent ID and API key from environment variables
agent_id = os.getenv("AGENT1_ID")
api_key = os.getenv("ELEVENLABS_API_KEY1")

# Create the ElevenLabs client instance
client = ElevenLabs(api_key=api_key)

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
    callback_user_transcript=lambda transcript: print(f"User: {transcript}"),

    # Uncomment if you want to see latency measurements
    # callback_latency_measurement=lambda latency: print(f"Latency: {latency}ms"),
)

# Start the conversation
conversation.start_session()

# Add signal handler for clean shutdown on Ctrl+C
signal.signal(signal.SIGINT, lambda sig, frame: conversation.end_session())

# Wait for the conversation to end and print the conversation ID
conversation_id = None # Initialize conversation_id
try:
    print("Waiting for session to end...")
    conversation_id = conversation.wait_for_session_end()
    print(f"Session ended. Conversation ID: {conversation_id}")
except OSError as e:
    print(f"Caught OSError during session end: {e}")
    # Attempt to get the ID anyway, it might have been set before the error
    # Assuming the Conversation object stores the ID in an accessible attribute like 'conversation_id'
    # You might need to check the library's source or documentation for the exact attribute name
    if hasattr(conversation, 'conversation_id'):
        conversation_id = conversation.conversation_id
    if conversation_id:
        print(f"Retrieved Conversation ID after error: {conversation_id}")
    else:
        print("Could not retrieve Conversation ID after error.")
except Exception as e:
    print(f"Caught unexpected Exception during session end: {e}")
    import traceback
    traceback.print_exc()
    # Try to get ID here too
    if hasattr(conversation, 'conversation_id'):
        conversation_id = conversation.conversation_id
    if conversation_id:
        print(f"Retrieved Conversation ID after unexpected error: {conversation_id}")
    else:
        print("Could not retrieve Conversation ID after unexpected error.")

# Proceed only if we have a conversation ID
if conversation_id:
    # New code to save conversation history
    print("Attempting to save conversation history...")
    try:
        # Get conversation details
        print(f"Fetching details for conversation: {conversation_id}")
        # Add a small delay in case the conversation data isn't immediately available
        time.sleep(2) # Wait 2 seconds
        conv_data = client.conversational_ai.get_conversation(conversation_id)
        print(f"Received data: {conv_data}")

        transcript = conv_data.get('transcript', None)

        if transcript is None:
            print("Error: Transcript not found in API response.")
            # Don't exit, just report the issue
        elif not transcript:
            print("Warning: Transcript is empty.")
        else:
            # Format conversation history
            history = []
            for entry in transcript:
                role = "User" if entry.get('role') == 'user' else "Agent"
                message = entry.get('message', '[message missing]')
                history.append(f"{role}: {message}")

            print(f"Formatted history:\n" + "\n".join(history))

            # Write to file
            filename = f"conversation_{conversation_id}.txt"
            print(f"Attempting to write to file: {filename}")
            # Added encoding='utf-8' for broader character support
            with open(filename, 'w', encoding='utf-8') as f:
                f.write('\n'.join(history))

            print(f"Conversation successfully saved to {filename}")

    except Exception as e:
        # Print the full error traceback for more details
        import traceback
        print(f"Failed to save conversation. Error: {str(e)}")
        print("Traceback:")
        traceback.print_exc()
else:
    print("Skipping conversation save because Conversation ID was not obtained.")

# The original except block for the history saving part is now nested
# within the 'if conversation_id:' block.
# The outer try...except handles errors from wait_for_session_end() 
# demo_full_loop.py

import os
import signal
import json
import time
from dotenv import load_dotenv

# Import ONLY what's needed for the conversation itself
from src.emotion_analysis import get_emotion_and_check_escalation
from src.coping_strategies import get_coping_advice

from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface

print("--- Loading Environment Variables (.env) --- ")
load_dotenv() # Load .env file

# --- Configuration --- 
print("--- Reading Configuration (API Keys, Agent ID) --- ")
agent_id = os.getenv("AGENT_ID")
api_key = os.getenv("ELEVENLABS_API_KEY")

if not agent_id or not api_key:
    print("\n*** ERROR: AGENT_ID and ELEVENLABS_API_KEY must be set. ***")
    exit()
else:
    print("   AGENT_ID found.")
    print("   ELEVENLABS_API_KEY found.")

print("--- Configuring ElevenLabs Client --- ")
client = ElevenLabs(api_key=api_key)

# --- Real-time Processing Function (Keep as is) --- 
def process_user_transcript_for_demo(transcript: str):
    """
    Processes the user's transcript in real-time for the demo,
    performs basic emotion analysis, checks for escalation,
    and prints relevant information or advice clearly.
    """
    print(f"\nUser said: " + "-"*20)
    print(f"{transcript}")
    print("-"*31)
    
    print(" -> Performing real-time analysis (TextBlob)...")
    emotion, escalation_needed = get_emotion_and_check_escalation(transcript)
    print(f"    >> Basic Emotion: {emotion}")
    print(f"    >> Escalation Keywords Found: {escalation_needed}")

    if escalation_needed:
        print("    >> ACTION: Potential escalation keywords detected! (Refer to crisis resources)")
    else:
        advice = get_coping_advice(emotion)
        print(f"    >> ACTION: Coping suggestion based on emotion: {advice}")
    print("-"*31)

# --- Initialize Conversation --- 
print("\n--- Initializing ElevenLabs Conversation Object --- ")
conversation = Conversation(
    client,
    agent_id,
    requires_auth=bool(api_key),
    audio_interface=DefaultAudioInterface(),
    callback_agent_response=lambda response: print(f"\nAgent said: " + "-"*20 + f"\n{response}\n" + "-"*31),
    callback_agent_response_correction=lambda original, corrected: print(f"\nAgent corrected: " + "-"*13 + f"\nOriginal: {original}\nCorrected: {corrected}\n" + "-"*31),
    callback_user_transcript=process_user_transcript_for_demo, # Use the demo version
)

# --- Main Demo Execution Flow --- 
print("\n===========================================")
print("     STARTING AI COMPANION DEMO (LIVE ONLY) ")
print("===========================================")
print("\n1. LIVE CONVERSATION PHASE")
print("   Speak into your microphone after the agent greets you.")
print("   Press Ctrl+C when you want to end the conversation.")
print("   NOTE: Post-processing now handled by watcher_processor.py")


signal.signal(signal.SIGINT, lambda sig, frame: conversation.end_session())

try:
    conversation.start_session()
    print("\n   Waiting for conversation to end (Press Ctrl+C)...")
    # We still call wait_for_session_end to block until Ctrl+C
    # but we don't need the return value or complex error handling here.
    conversation.wait_for_session_end()
    print(f"\n   Conversation session ended attempt.") 

except OSError as e:
    # Log the expected error but don't stop everything
    print(f"\n   Caught expected OSError during session end (likely audio stream): {e}")
    print("   This is often okay, the watcher script will handle processing.")
except Exception as e:
    print(f"\n   Caught unexpected Exception during session end: {e}")
    import traceback
    traceback.print_exc()

print("\n===========================================")
print("        LIVE CONVERSATION DEMO ENDED       ")
print("===========================================")
print("Run watcher_processor.py in another terminal to process the conversation.") 
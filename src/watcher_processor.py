# watcher_processor.py

import os
import time
import json
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

# Import processing functions from src
from src.analyzer_agent import analyze_and_save_profile
from src.knowledge_uploader import upload_profile_file

print("--- Watcher/Processor Started ---")

# --- Configuration --- 
print("--- Loading Environment Variables (.env) --- ")
load_dotenv()

agent_id = os.getenv("AGENT_ID")
api_key = os.getenv("ELEVENLABS_API_KEY")

if not agent_id or not api_key:
    print("\n*** ERROR: AGENT_ID and ELEVENLABS_API_KEY must be set. ***")
    exit()

print("--- Configuring ElevenLabs Client --- ")
client = ElevenLabs(api_key=api_key)

# --- State Management --- 
PROCESSED_IDS_FILE = "processed_conversation_ids.txt"
processed_ids = set()

def load_processed_ids():
    """Loads previously processed IDs from a file."""
    if os.path.exists(PROCESSED_IDS_FILE):
        try:
            with open(PROCESSED_IDS_FILE, 'r') as f:
                for line in f:
                    processed_ids.add(line.strip())
            print(f"--- Loaded {len(processed_ids)} previously processed IDs ---")
        except Exception as e:
            print(f"Warning: Could not load processed IDs file: {e}")
    else:
        print("--- No processed IDs file found, starting fresh. ---")

def save_processed_id(conversation_id):
    """Appends a newly processed ID to the file."""
    try:
        with open(PROCESSED_IDS_FILE, 'a') as f:
            f.write(conversation_id + '\n')
        processed_ids.add(conversation_id)
    except Exception as e:
        print(f"Warning: Could not save processed ID {conversation_id}: {e}")

# --- Core Processing Function --- 
def process_conversation(conversation_id: str):
    """Fetches, saves, analyzes, and uploads a single conversation."""
    print(f"\n>>> Processing NEW Conversation ID: {conversation_id} <<<")
    transcript_filepath = None
    profile_filepath = None
    
    try:
        # 1. Get and Save Transcript
        print(f"   [Step 1/3] Fetching transcript for {conversation_id}...")
        time.sleep(1) # Small delay before fetching
        conv_data = client.conversational_ai.get_conversation(conversation_id)
        
        # FIX: Access attribute directly, check existence
        transcript_entries = None
        if hasattr(conv_data, 'transcript'):
             transcript_entries = conv_data.transcript
        else:
             print(f"Warning: Conversation data object for {conversation_id} missing 'transcript' attribute.")

        if transcript_entries:
            history = []
            # FIX: Check entry type and access attributes
            for entry in transcript_entries:
                role = "Agent" # Default role
                message = "[message missing]"
                if hasattr(entry, 'role') and entry.role == 'user':
                    role = "User"
                if hasattr(entry, 'message'):
                    message = entry.message
                history.append(f"{role}: {message}")

            conv_dir = "conversations"
            os.makedirs(conv_dir, exist_ok=True)
            timestamp = time.strftime("%Y%m%d_%H%M%S") # Timestamp of processing
            transcript_filename = f"conversation_{conversation_id}_{timestamp}.txt"
            transcript_filepath = os.path.join(conv_dir, transcript_filename)
            
            with open(transcript_filepath, 'w', encoding='utf-8') as f:
                f.write('\n'.join(history))
            print(f"      Transcript saved to: {transcript_filepath}")
        else:
             print("      Warning: Transcript not found or empty in API response.")
             return # Cannot proceed without transcript

        # 2. Analyze Transcript and Save Profile
        print(f"   [Step 2/3] Analyzing transcript with LLM...")
        if transcript_filepath:
            profile_filepath = analyze_and_save_profile(transcript_filepath)
            if not profile_filepath:
                print("      Warning: Profile generation failed.")
                # Decide if we should still mark as processed or retry later?
                # For now, we'll continue to upload if profile exists, else mark processed.
        else:
            print("      Error: Transcript path not available for analysis.")
            return # Should not happen if step 1 succeeded

        # 3. Upload Profile to Knowledge Base
        print(f"   [Step 3/3] Uploading profile to Knowledge Base...")
        if profile_filepath:
            upload_profile_file(profile_filepath)
            # Assuming upload_profile_file prints success/failure
        else:
            print("      Skipping KB upload as profile was not generated/saved.")
        
        # Mark as processed if we got this far, even if upload failed (to avoid retries)
        save_processed_id(conversation_id)
        print(f"<<< Finished processing {conversation_id} >>>")
        
    except Exception as e:
        import traceback
        print(f"\n*** ERROR processing conversation {conversation_id}: {str(e)} ***")
        print("Traceback:")
        traceback.print_exc()
        # Optionally, don't save ID here to retry later

# --- Main Watcher Loop --- 
CHECK_INTERVAL_SECONDS = 60 # Check every 60 seconds

if __name__ == "__main__":
    load_processed_ids()
    print(f"--- Starting watcher loop (checking every {CHECK_INTERVAL_SECONDS} seconds) ---")
    
    while True:
        print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Checking for new conversations...")
        try:
            # Fetch recent conversations (e.g., last 10)
            # Note: Check API docs for sorting/filtering options if available
            # We fetch a few in case multiple finished between checks
            recent_conversations = client.conversational_ai.get_conversations()
            
            found_new = 0
            if recent_conversations and hasattr(recent_conversations, 'conversations'):
                for conv_summary in recent_conversations.conversations:
                    # FIX: Access attribute directly, not like a dictionary
                    # Add a check for the attribute's existence for safety
                    conv_id = None
                    if hasattr(conv_summary, 'conversation_id'):
                         conv_id = conv_summary.conversation_id 
                    else:
                         print("Warning: Conversation summary object missing 'conversation_id' attribute.")
                         continue # Skip this summary

                    if conv_id and conv_id not in processed_ids:
                        # Found a new one to process
                        found_new += 1
                        process_conversation(conv_id)
                        time.sleep(2) # Small pause between processing multiple
            
            if found_new == 0:
                print("   No new conversations found.")
                
        except Exception as loop_err:
            print(f"\n*** ERROR in watcher loop: {loop_err} ***")
            # Consider adding more robust error handling (e.g., backoff)
            
        # Wait for the next check
        time.sleep(CHECK_INTERVAL_SECONDS) 
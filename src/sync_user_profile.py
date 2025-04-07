import os
import time
import schedule
from datetime import datetime
import glob
from knowledge_uploader import process_profiles

def sync_profiles():
    """Sync all profiles to ElevenLabs."""
    print(f"\n[{datetime.now()}] Starting profile sync...")
    process_profiles()
    print(f"[{datetime.now()}] Profile sync completed.")

def check_new_conversations():
    """Check for new conversations and sync if found."""
    # Get the latest conversation file
    conversation_files = glob.glob("conversations/*.txt")
    if not conversation_files:
        return
        
    latest_conversation = max(conversation_files, key=os.path.getctime)
    latest_time = os.path.getctime(latest_conversation)
    
    # If conversation is less than 5 minutes old, sync profiles
    if time.time() - latest_time < 300:  # 300 seconds = 5 minutes
        print(f"\n[{datetime.now()}] New conversation detected, syncing profiles...")
        sync_profiles()

def main():
    # Schedule sync every 2 days at 6 AM
    schedule.every(2).days.at("06:00").do(sync_profiles)
    
    # Check for new conversations every 5 minutes
    schedule.every(5).minutes.do(check_new_conversations)
    
    print("Profile sync scheduler started.")
    print("Will run every 2 days at 6 AM and after new conversations.")
    print("Press Ctrl+C to exit.")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main() 
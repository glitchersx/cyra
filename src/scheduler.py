import schedule
import time
import os
from datetime import datetime
import glob

def analyze_new_transcripts():
    """Find and analyze any new transcripts in the conversations directory."""
    print(f"\n[{datetime.now()}] Starting scheduled analysis...")
    
    # Get all .txt files in conversations directory
    transcript_files = glob.glob("conversations/*.txt")
    
    if not transcript_files:
        print("No new transcripts found.")
        return
        
    for transcript_file in transcript_files:
        print(f"Analyzing {transcript_file}...")
        os.system(f"python analyzer_agent.py {transcript_file}")

# Schedule the job to run daily at 6 AM
schedule.every().day.at("06:00").do(analyze_new_transcripts)

print("Scheduler started. Will run daily at 6 AM.")
print("Press Ctrl+C to exit.")

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute 
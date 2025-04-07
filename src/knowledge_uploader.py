import os
import json
import requests
import glob
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def format_profile_to_text(profile_data: dict) -> str:
    """Convert JSON profile to natural text format."""
    text = f"""
User Profile Analysis:
Name: {profile_data.get('user_name', 'Unknown')}
Current Mood: {profile_data.get('mood', 'neutral')}
Emotion Trend: {profile_data.get('emotion_trend', 'stable')}
Key Topics: {', '.join(profile_data.get('topics', []))}
Profile Tags: {', '.join(profile_data.get('profile_tags', []))}
Summary: {profile_data.get('persona_summary', 'No summary available')}
"""
    return text.strip()

def upload_to_elevenlabs(text_content: str, profile_name: str) -> bool:
    """Upload profile to ElevenLabs Conversational AI."""
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        print("Error: ELEVENLABS_API_KEY not found in environment variables.")
        return False

    url = "https://api.elevenlabs.io/v1/convai/knowledge-base/text"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    
    data = {
        "text": text_content,
        "name": profile_name
    }

    print(f"--- Uploading profile '{profile_name}' to ElevenLabs KB... ---")
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        print(f"--- Successfully uploaded profile: {profile_name} ---")
        return True
    except requests.exceptions.RequestException as e:
        print(f"--- Failed to upload profile '{profile_name}'. Status code: {e.response.status_code if e.response else 'N/A'} ---")
        print(f"Response: {e.response.text if e.response else 'No response'}")
        return False
    except Exception as e:
        print(f"--- Error uploading profile '{profile_name}': {e} ---")
        return False

def upload_profile_file(profile_filepath: str):
    """Reads a profile JSON file, formats it, and uploads it."""
    if not profile_filepath or not os.path.exists(profile_filepath):
        print(f"Error: Profile file not found or invalid path: {profile_filepath}")
        return

    print(f"--- Processing profile file for upload: {profile_filepath} ---")
    try:
        with open(profile_filepath, 'r', encoding='utf-8') as f:
            profile_data = json.load(f)
        
        # Format profile data into text
        text_content = format_profile_to_text(profile_data)
        
        # Create profile name from filename
        profile_name = f"User Profile - {os.path.basename(profile_filepath)}"
        
        # Upload to ElevenLabs
        if upload_to_elevenlabs(text_content, profile_name):
            print(f"--- Successfully processed and uploaded {profile_filepath} ---")
        else:
            print(f"--- Failed to upload {profile_filepath} ---")
            
    except Exception as e:
        print(f"Error processing profile file {profile_filepath}: {e}")

def process_profiles():
    """Process all JSON profiles in user_profiles directory."""
    print("--- Starting batch profile processing and upload... ---")
    profile_files = glob.glob("user_profiles/*.json")
    if not profile_files:
        print("No profiles found in user_profiles directory.")
        return
    
    success_count = 0
    failure_count = 0
    for profile_file in profile_files:
        if upload_profile_file(profile_file):
             success_count += 1
        else:
             failure_count += 1
    print(f"--- Batch upload complete. Success: {success_count}, Failures: {failure_count} ---")

if __name__ == "__main__":
    process_profiles() 
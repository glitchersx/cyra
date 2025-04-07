import os
import json
import time
import argparse
from groq import Groq
from dotenv import load_dotenv

load_dotenv() # Load .env file for API keys

def read_transcript(filepath: str) -> str:
    """Reads the content of a transcript file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Transcript file not found at {filepath}")
        return None
    except Exception as e:
        print(f"Error reading transcript file {filepath}: {e}")
        return None

def analyze_transcript_with_llama(transcript: str, api_key: str) -> dict | None:
    """
    Analyzes the transcript using Llama 4 via Groq API to extract profile info.
    """
    if not api_key:
        print("Error: GROQ_API_KEY not found in environment variables.")
        return None
        
    client = Groq(api_key=api_key)

    # --- Prompt Engineering ---
    # This is the crucial part. We need to instruct Llama 4 precisely
    # what to extract and the exact JSON format required.
    prompt = f"""
Analyze the following conversation transcript. Based *only* on the content of the transcript, generate a JSON object containing the following fields:
- "user_name": Infer the user's name if mentioned, otherwise use "Unknown".
- "mood": Identify the dominant overall mood (e.g., "lonely", "anxious", "grateful", "neutral", "sad", "frustrated", "happy").
- "emotion_trend": Describe any noticeable shift in emotion during the conversation (e.g., "started sad, ended neutral", "consistently positive", "increasing frustration").
- "topics": List key topics discussed (e.g., ["family", "work stress", "health concerns", "hobbies", "memories"]). Max 5 topics.
- "profile_tags": Generate 3-5 relevant tags describing the user's potential situation or personality based on the conversation (e.g., ["#grieving", "#seeking_reassurance", "#storyteller", "#caregiver", "#optimistic"]). Use hashtags.
- "persona_summary": Write a brief (1-2 sentences) summary capturing the essence of the user's state and potential needs as revealed *in this conversation*.

**IMPORTANT RULES:**
1. Respond *only* with the valid JSON object. Do not include any explanatory text before or after the JSON.
2. If a field cannot be determined from the transcript, use a reasonable default (like "Unknown", "neutral", empty list [], or a generic statement).
3. Base the analysis *strictly* on the provided transcript text. Do not invent information.

Transcript:
---
{transcript}
---

JSON Output:
"""

    print("\n--- Sending request to Groq API for analysis... ---")
    try:
        completion = client.chat.completions.create(
            # model="meta-llama/llama-4-scout-17b-16e-instruct", # Your example model
            model="llama3-70b-8192", # Using a generally available Llama 3 model on Groq
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
                # No assistant message needed here as we provide full instructions
            ],
            temperature=0.5, # Lower temperature for more deterministic JSON output
            max_tokens=1024, # Adjust as needed
            top_p=1,
            stream=False, # Get the full response at once for easier JSON parsing
            stop=None, # Model should stop naturally after generating JSON
            # response_format={"type": "json_object"} # If supported by model/Groq, enforce JSON output
        )

        response_content = completion.choices[0].message.content
        print("--- Groq API Analysis Response Received ---")
        # print(response_content) # Optional: print raw response for debugging

        # Attempt to parse the JSON response
        # It might be necessary to clean up potential markdown code blocks (```json ... ```)
        if response_content.startswith("```json"):
             response_content = response_content[7:-3].strip() # Remove markdown fences
        elif response_content.startswith("```"):
             response_content = response_content[3:-3].strip()

        profile_data = json.loads(response_content)
        return profile_data

    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON response from Groq API: {e}")
        print("Received content was:\n", response_content)
        return None
    except Exception as e:
        print(f"Error interacting with Groq API: {e}")
        import traceback
        traceback.print_exc()
        return None

def save_profile(profile_data: dict, transcript_filepath: str) -> str | None:
    """Saves the generated profile data to a JSON file. Returns the path if successful."""
    try:
        # Use absolute path of transcript to find the base directory
        abs_transcript_path = os.path.abspath(transcript_filepath)
        base_dir = os.path.dirname(abs_transcript_path)
        project_root = os.path.dirname(base_dir) # Assumes conversations dir is one level down
        profile_dir = os.path.join(project_root, "user_profiles")
        os.makedirs(profile_dir, exist_ok=True)

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        # Extract original conversation ID/timestamp from transcript filename for linkage
        transcript_filename = os.path.basename(transcript_filepath)
        # Handle potential '.txt' extension
        base_transcript_name = transcript_filename.rsplit('.', 1)[0]
        profile_filename = f"user_profile_{base_transcript_name}_{timestamp}.json"
        profile_filepath = os.path.join(profile_dir, profile_filename)

        with open(profile_filepath, 'w', encoding='utf-8') as f:
            json.dump(profile_data, f, indent=2)
        print(f"--- Successfully saved user profile to {profile_filepath} ---")
        return profile_filepath
    except Exception as e:
        print(f"Error saving user profile: {e}")
        return None

# NEW FUNCTION TO BE CALLED EXTERNALLY
def analyze_and_save_profile(transcript_filepath: str) -> str | None:
    """Reads a transcript, analyzes it, and saves the profile. Returns profile path."""
    print(f"--- Starting analysis for transcript: {transcript_filepath} ---")
    transcript_content = read_transcript(transcript_filepath)
    if not transcript_content:
        return None

    # Load Groq API key from environment
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
         print("Error: GROQ_API_KEY environment variable not set.")
         return None

    profile_data = analyze_transcript_with_llama(transcript_content, groq_api_key)

    if profile_data:
        profile_filepath = save_profile(profile_data, transcript_filepath)
        return profile_filepath
    else:
        print("--- Failed to generate user profile data from analysis. ---")
        return None

# Keep the main block for potential direct script execution/testing
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze conversation transcript using Llama 4 via Groq.")
    parser.add_argument("transcript_file", help="Path to the conversation transcript .txt file.")
    args = parser.parse_args()

    # Validate input file path
    if not os.path.exists(args.transcript_file) or not args.transcript_file.endswith(".txt"):
        print(f"Error: Invalid transcript file path: {args.transcript_file}")
    else:
        analyze_and_save_profile(args.transcript_file) 
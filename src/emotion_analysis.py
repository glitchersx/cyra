import argparse
import os
from textblob import TextBlob

# Keywords that might indicate a need for escalation or specific support
escalation_keywords = [
    "kill myself", "suicide", "end it all", "can't go on", "hopeless",
    "want to die", "goodbye cruel world", "no reason to live",
    # Add more sensitive terms carefully
    "self-harm", "hurting myself"
]

def get_emotion_and_check_escalation(text: str):
    """Analyzes text for basic sentiment and checks for escalation keywords."""
    # Basic Sentiment Analysis
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    # Categorize sentiment
    if polarity > 0.1:
        emotion_label = "positive"
    elif polarity < -0.1:
        emotion_label = "negative"
    else:
        emotion_label = "neutral"

    # Check for escalation keywords (case-insensitive)
    escalation_needed = False
    lower_text = text.lower()
    for keyword in escalation_keywords:
        if keyword in lower_text:
            escalation_needed = True
            break # Stop checking once one keyword is found

    return emotion_label, escalation_needed

# NEW FUNCTION: Analyzes a whole file
def analyze_transcript_file(filepath: str):
    """Reads a transcript file and prints its overall emotion analysis."""
    print(f"--- Analyzing file: {filepath} ---")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        if not content:
            print("Error: File is empty.")
            return

        # Analyze the entire content using the existing function
        emotion, escalation_needed = get_emotion_and_check_escalation(content)

        print(f"  Overall Emotion Detected: {emotion}")
        print(f"  Potential Escalation Needed: {escalation_needed}")

    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
    except Exception as e:
        print(f"Error reading or processing file {filepath}: {e}")

# UPDATED: Main execution block for command-line use
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyze overall emotion and check for escalation keywords in a saved conversation transcript file."
    )
    parser.add_argument(
        "filepath",
        help="Path to the transcript file (e.g., conversations/conversation_xyz.txt)"
    )
    args = parser.parse_args()

    # Basic validation
    if not os.path.exists(args.filepath):
        print(f"Error: The file '{args.filepath}' does not exist.")
    elif not args.filepath.endswith(".txt"):
        print(f"Error: Input file should be a .txt file.")
    # Optional: Check if it's in the expected directory
    # elif not args.filepath.startswith("conversations/"):
    #     print(f"Warning: File might not be in the expected 'conversations' directory.")
    #     analyze_transcript_file(args.filepath)
    else:
        analyze_transcript_file(args.filepath)

# (Keep the existing get_emotion function for now if needed elsewhere, 
# or remove if get_emotion_and_check_escalation replaces its use cases)

def get_emotion(text: str) -> str:
    """
    Analyzes the sentiment of the text using TextBlob and returns a
    simple emotion label based on polarity.

    Args:
        text: The input text (e.g., user's speech transcript).

    Returns:
        A simple emotion label: "positive", "negative", or "neutral".
    """
    if not text:
        return "neutral" # Handle empty input

    try:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity

        # Simple mapping based on polarity score
        if polarity > 0.1:  # Threshold can be adjusted
            return "positive"
        elif polarity < -0.1: # Threshold can be adjusted
            return "negative"
        else:
            return "neutral"
            
    except Exception as e:
        print(f"Error during sentiment analysis: {e}")
        return "neutral" # Default to neutral on error

# Example Usage (for testing)
if __name__ == '__main__':
    sample_text_positive = "I am feeling really happy and wonderful today!"
    sample_text_negative = "This is terrible, I feel awful and sad."
    sample_text_neutral = "The weather is okay."

    print(f"'{sample_text_positive}' -> Emotion: {get_emotion(sample_text_positive)}")
    print(f"'{sample_text_negative}' -> Emotion: {get_emotion(sample_text_negative)}")
    print(f"'{sample_text_neutral}' -> Emotion: {get_emotion(sample_text_neutral)}")

    # Test escalation
    test_escalate_keyword = "I feel hopeless and want to end my life maybe."
    test_escalate_negative = "Everything is just awful and pointless and horrible beyond belief."
    test_normal_negative = "I had a bad day."

    emotion_kw, escalate_kw = get_emotion_and_check_escalation(test_escalate_keyword)
    print(f"\n'{test_escalate_keyword}' -> Emotion: {emotion_kw}, Escalate: {escalate_kw}")

    emotion_neg, escalate_neg = get_emotion_and_check_escalation(test_escalate_negative)
    print(f"'{test_escalate_negative}' -> Emotion: {emotion_neg}, Escalate: {escalate_neg}")

    emotion_norm, escalate_norm = get_emotion_and_check_escalation(test_normal_negative)
    print(f"'{test_normal_negative}' -> Emotion: {emotion_norm}, Escalate: {escalate_norm}") 
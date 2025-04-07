from textblob import TextBlob

# NEW: Define keywords for escalation check
# WARNING: This is a very basic list and not exhaustive. Proper crisis detection is complex.
ESCALATION_KEYWORDS = {
    "suicide", "kill myself", "end my life", "hopeless", "can't go on", 
    "want to die", "not worth living"
    # Add more relevant terms carefully
}

def get_emotion_and_check_escalation(text: str) -> tuple[str, bool]:
    """
    Analyzes sentiment, checks for escalation keywords.

    Args:
        text: The input text.

    Returns:
        A tuple containing:
            - str: Emotion label ("positive", "negative", "neutral").
            - bool: True if escalation criteria met, False otherwise.
    """
    if not text:
        return "neutral", False

    escalation_needed = False
    emotion = "neutral"
    
    try:
        # Check for keywords first (case-insensitive)
        lower_text = text.lower()
        if any(keyword in lower_text for keyword in ESCALATION_KEYWORDS):
            escalation_needed = True
            # Optional: Force emotion to negative if keywords found?
            # emotion = "negative"
            
        # Perform sentiment analysis
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity

        # Determine emotion label
        if polarity > 0.1: 
            emotion = "positive"
        elif polarity < -0.1:
            emotion = "negative"
            # Optional: Add escalation based on very low polarity?
            # if polarity < -0.8: # Example threshold
            #     escalation_needed = True
        else:
            emotion = "neutral"
            
    except Exception as e:
        print(f"Error during sentiment analysis/escalation check: {e}")
        # Default to neutral, no escalation on error
        return "neutral", False 
        
    return emotion, escalation_needed

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
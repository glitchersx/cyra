import random

# Dictionary mapping simple emotion labels to coping strategies or affirmations
COPING_STRATEGIES = {
    "positive": [
        "That's wonderful to hear! Keep embracing that positivity.",
        "It's great that you're feeling good. What's bringing you joy right now?",
        "Hold onto that positive feeling! Remember what contributes to it.",
        "Sounds like you're in a great headspace. Keep shining!"
    ],
    "negative": [
        "I'm sorry to hear you're feeling this way. Remember to be kind to yourself.",
        "It's okay to feel down sometimes. Try taking a few deep breaths.",
        "Focus on one small thing you can control right now. Even a small step helps.",
        "Remember that feelings are temporary. Can you think of one thing that usually makes you feel a bit better?",
        "Consider reaching out to someone you trust, or perhaps engage in a calming activity."
    ],
    "neutral": [
        "Thanks for sharing. Is there anything specific on your mind?",
        "Okay, understood. How is your day going overall?",
        "Sometimes just being is okay. No need to force a feeling."
    ]
}

def get_coping_advice(emotion: str) -> str:
    """
    Selects a random coping strategy or affirmation based on the detected emotion.

    Args:
        emotion: The detected emotion label ("positive", "negative", "neutral").

    Returns:
        A randomly selected piece of advice or affirmation corresponding to the emotion,
        or a default message if the emotion is not recognized.
    """
    advice_list = COPING_STRATEGIES.get(emotion)
    if advice_list:
        return random.choice(advice_list)
    else:
        # Fallback for unrecognized emotion strings (shouldn't happen with current setup)
        return "It's important to acknowledge how you feel. Tell me more if you like."

# Example Usage (for testing)
if __name__ == '__main__':
    print(f"Positive advice: {get_coping_advice('positive')}")
    print(f"Negative advice: {get_coping_advice('negative')}")
    print(f"Neutral advice: {get_coping_advice('neutral')}")
    print(f"Unknown advice: {get_coping_advice('confused')}") 
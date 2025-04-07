import os
import json
import glob
from datetime import datetime, timedelta
from flask import Flask, jsonify

# NEW: Set Matplotlib backend *before* importing pyplot
import matplotlib
matplotlib.use('Agg') # Use non-interactive backend
import matplotlib.pyplot as plt

import numpy as np

app = Flask(__name__)

# Mood categories and their weights
MOOD_CATEGORIES = {
    "Withdrawn": -2,
    "Open": 2,
    "Angry": -1,
    "Anxious": -1,
    "Hopeful": 2
}

def analyze_mood_trend(profile_data: dict) -> str:
    """Analyze mood trend from profile data."""
    mood = profile_data.get('mood', 'neutral').lower()
    emotion_trend = profile_data.get('emotion_trend', 'stable')
    
    # Basic trend analysis
    if 'increasing' in emotion_trend.lower():
        return "mood worsening"
    elif 'decreasing' in emotion_trend.lower():
        return "mood improving"
    elif 'stable' in emotion_trend.lower():
        return "mood stable"
    return "mood neutral"

def calculate_mood_score(profile_data: dict) -> float:
    """Calculate a numerical score for the mood."""
    mood = profile_data.get('mood', 'neutral').lower()
    tags = profile_data.get('profile_tags', [])
    
    # Base score from mood
    score = 0
    if mood in ['happy', 'hopeful']:
        score = 2
    elif mood in ['sad', 'lonely', 'anxious']:
        score = -1
    elif mood == 'neutral':
        score = 0
    
    # Adjust score based on tags
    for tag in tags:
        tag = tag.lower().replace('#', '')
        if tag in MOOD_CATEGORIES:
            score += MOOD_CATEGORIES[tag]
    
    return score

def generate_mood_insight(profiles: list) -> str:
    """Generate insight text based on mood trends."""
    if len(profiles) < 2:
        return "Insufficient data for mood analysis"
    
    recent_score = calculate_mood_score(profiles[-1])
    previous_score = calculate_mood_score(profiles[-2])
    
    if recent_score > previous_score:
        return "You seem more positive than last time"
    elif recent_score < previous_score:
        return "You seem less positive than last time"
    else:
        return "Your mood has remained stable"

def create_mood_graph(profiles: list):
    """Create a mood vs time graph."""
    dates = []
    scores = []
    
    for profile in profiles:
        try:
            # Extract date string (YYYYMMDD_HHMMSS) from filename
            filename = profile.get('filename', '')
            parts = filename.replace('.json', '').split('_')
            if len(parts) >= 2:
                 # Combine the last two parts assuming format YYYYMMDD_HHMMSS
                 date_str = f"{parts[-2]}_{parts[-1]}"
                 # Use the correct format string for parsing
                 date = datetime.strptime(date_str, '%Y%m%d_%H%M%S')
                 dates.append(date)
                 scores.append(calculate_mood_score(profile))
            else:
                print(f"Warning: Could not parse date from filename format: {filename}")
                continue
        except ValueError:
            print(f"Warning: Error parsing date string '{date_str}' from filename: {filename}")
            continue # Skip profile if date cannot be parsed

    if not dates or len(dates) < 2: # Need at least two points to plot
        print("Warning: Not enough data points with valid dates to create graph.")
        return None
    
    plt.figure(figsize=(10, 6))
    plt.plot(dates, scores, marker='o')
    plt.title('Mood Evolution Over Time')
    plt.xlabel('Date')
    plt.ylabel('Mood Score')
    plt.grid(True)
    plt.xticks(rotation=45)
    
    # Save the graph
    graph_path = 'mood_evolution.png'
    plt.savefig(graph_path)
    plt.close()
    
    return graph_path

@app.route('/mood-trends', methods=['GET'])
def get_mood_trends():
    """API endpoint to get mood trends data."""
    # Get all profile files
    profile_files = glob.glob("user_profiles/*.json")
    profiles = []
    dates_for_json = [] # Store correctly extracted date strings for response

    for file in profile_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                profile_data = json.load(f)
                filename = os.path.basename(file)
                profile_data['filename'] = filename # Add filename for sorting/parsing

                 # Extract date string (YYYYMMDD_HHMMSS) from filename for sorting and response
                parts = filename.replace('.json', '').split('_')
                if len(parts) >= 2:
                    date_str = f"{parts[-2]}_{parts[-1]}"
                    # Validate date string format before adding
                    datetime.strptime(date_str, '%Y%m%d_%H%M%S') # Raises ValueError if wrong format
                    profile_data['sort_key'] = date_str # Use for sorting
                    profiles.append(profile_data)
                    dates_for_json.append(date_str) # Add correct string to list
                else:
                     print(f"Warning: Skipping file due to unexpected filename format: {filename}")

        except (json.JSONDecodeError, ValueError, FileNotFoundError) as e:
             print(f"Warning: Error processing file {file}: {e}")
             continue # Skip problematic files

    # Sort profiles by the extracted date string
    profiles.sort(key=lambda x: x.get('sort_key', ''))

    # Generate insights and graph
    insight = generate_mood_insight(profiles)
    graph_path = create_mood_graph(profiles)
    mood_scores = [calculate_mood_score(p) for p in profiles] # Recalculate based on sorted list

    # Prepare response with corrected dates
    response = {
        'insight': insight,
        'graph_path': graph_path, # This should now be 'mood_evolution.png' if successful
        'mood_scores': mood_scores,
        'dates': dates_for_json # Use the correctly extracted date strings
    }

    return jsonify(response)

def analyze_emotional_degradation(profiles: list) -> str:
    """Analyze if there's emotional degradation over time."""
    if len(profiles) < 7:  # Need at least 7 days of data
        return "Insufficient data for trend analysis"
    
    recent_scores = [calculate_mood_score(p) for p in profiles[-7:]]
    if all(recent_scores[i] >= recent_scores[i+1] for i in range(len(recent_scores)-1)):
        return "Warning: Mood has been consistently worsening over the last 7 days"
    return "No significant degradation detected"

if __name__ == "__main__":
    app.run(debug=True, port=5000) 
# ✅ AI Companion - Hackathon MVP Build Plan

## 🧠 Phase 1: Clean the Codebase
- [ ] Remove agent2.py (keep just agent.py)
- [ ] Refactor agent.py to import emotion and coping strategy modules
- [ ] Ensure conversation_manager.py saves all sessions with timestamps

## 💬 Phase 2: Add Emotion Detection
- [ ] Create emotion_analysis.py
  - Use TextBlob or HuggingFace classifier (pref: HuggingFace emotion model)
  - Input: user text, Output: "sad", "happy", "angry", etc.
- [ ] Test emotion detection on sample inputs

## 🛟 Phase 3: Add Coping Strategies
- [ ] Create coping_strategies.py
  - Create a dictionary mapping emotions to advice arrays
- [ ] In agent.py, after emotion is detected → pull advice from this module

## 🚨 Phase 4: Escalation Logic
- [ ] If transcript contains suicide keywords or high negative score:
    - Output a serious message: “Would you like help?”
    - Provide hotline / contact professional popup on frontend

## 🎨 Phase 5: UI Makeover
- [ ] Install Tailwind in frontend
- [ ] Redesign with soft colors (sky blue, beige), large font, calming UX
- [ ] Voice button should be a glowing circle mic (centered)
- [ ] Show live emotion detection on screen (e.g. "You sound sad")
- [ ] Add journaling area (text + save to backend)
- [ ] Show conversation history in a right panel

## 🔗 Phase 6: Full Pipeline Test
- [ ] User speaks → STT → emotion analysis → coping advice → TTS
- [ ] Emotion label + advice visible in UI
- [ ] Conversation saved and viewable
- [ ] Escalation triggers tested

## 🚀 BONUS
- [ ] Add system memory (LangChain or simple DB)
- [ ] Add daily check-in: “How are you feeling today?”
- [ ] Add timeline of moods (optional graph UI)

import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

# ── Priority keyword rules (Python-side, no AI needed) ──────────────────
HIGH_KEYWORDS = [
    'electric', 'electricity', 'shock', 'short circuit', 'sparking',
    'power cut', 'no power', 'wiring', 'electrocute',
    'leak', 'leaking', 'water leak', 'pipe burst', 'burst pipe',
    'flood', 'flooding', 'overflow', 'sewage', 'no water',
    'fire', 'smoke', 'gas', 'fumes',
    'lock broken', 'broken lock', 'security', 'unsafe'
]

MEDIUM_KEYWORDS = [
    'wifi', 'internet', 'network', 'connectivity', 'router', 'slow internet',
    'fan', 'ac', 'air conditioner', 'cooler',
    'food', 'mess', 'meal', 'canteen', 'breakfast', 'lunch', 'dinner',
    'dirty', 'clean', 'cleaning', 'garbage', 'waste', 'hygiene', 'cockroach',
    'noise', 'loud', 'disturbance',
    'door', 'window', 'furniture', 'ceiling', 'wall', 'repair'
]

def get_priority_from_keywords(title: str, description: str) -> str:
    combined = (title + ' ' + description).lower()
    for word in HIGH_KEYWORDS:
        if word in combined:
            return 'High'
    for word in MEDIUM_KEYWORDS:
        if word in combined:
            return 'Medium'
    return 'Low'

def get_category_from_keywords(title: str, description: str) -> str:
    combined = (title + ' ' + description).lower()
    if any(w in combined for w in ['electric', 'electricity', 'shock', 'power', 'switch', 'socket', 'light', 'bulb', 'fan', 'wiring', 'sparking']):
        return 'Electrical'
    if any(w in combined for w in ['water', 'pipe', 'leak', 'tap', 'flush', 'drain', 'sewage', 'flood', 'plumb']):
        return 'Plumbing'
    if any(w in combined for w in ['wifi', 'internet', 'network', 'connectivity', 'router']):
        return 'Internet'
    if any(w in combined for w in ['dirty', 'clean', 'garbage', 'waste', 'hygiene', 'cockroach', 'pest', 'rat', 'mosquito']):
        return 'Cleanliness'
    if any(w in combined for w in ['food', 'mess', 'meal', 'canteen', 'breakfast', 'lunch', 'dinner', 'taste', 'cook']):
        return 'Food'
    if any(w in combined for w in ['door', 'window', 'furniture', 'ceiling', 'wall', 'repair', 'broken', 'damage', 'crack']):
        return 'Maintenance'
    return 'Other'

def generate_summary(title: str, description: str, category: str, priority: str) -> str:
    return f"{priority} priority {category} issue: {title[:60]}."

# ── Try Gemini AI, fall back to keyword logic if it fails ───────────────
def analyze_complaint(title: str, description: str) -> dict:

    # Always get keyword-based results as backup
    keyword_priority = get_priority_from_keywords(title, description)
    keyword_category = get_category_from_keywords(title, description)

    try:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

        # Try different model names until one works
        model = None
        model_names = [
            'gemini-2.0-flash',
            'gemini-2.0-flash-lite',
            'gemini-1.5-flash',
            'gemini-1.5-pro',
            'gemini-pro',
        ]
        for name in model_names:
            try:
                model = genai.GenerativeModel(name)
                test = model.generate_content("hi")
                break  # this model works
            except Exception:
                model = None
                continue

        if model is None:
            raise Exception("No working Gemini model found")

        prompt = f"""
You are a hostel grievance manager. Analyze this complaint.
Reply ONLY with raw JSON. No markdown, no extra text.

Title: {title}
Description: {description}

Priority rules:
- High: electricity, electric shock, water leaking, flooding, fire, no water, sewage, safety hazard, security issue
- Medium: wifi, internet, food quality, fan, AC, cleanliness, noise, minor repairs
- Low: suggestions, requests, general feedback, minor inconvenience

Category rules:
- Electrical: lights, fans, switches, power, electric, shock, sparking
- Plumbing: water, pipe, leak, tap, flush, drain, sewage, flood
- Internet: wifi, internet, network, router
- Cleanliness: dirty, garbage, hygiene, pest, cockroach
- Food: mess, meal, canteen, food quality
- Maintenance: door, window, furniture, repair, broken
- Other: anything else

JSON format:
{{
  "category": "Electrical or Plumbing or Internet or Cleanliness or Food or Maintenance or Other",
  "priority": "High or Medium or Low",
  "summary": "one sentence under 20 words"
}}
"""
        response = model.generate_content(prompt)
        text = response.text.strip()
        text = re.sub(r'```json|```', '', text).strip()
        ai_result = json.loads(text)

        # ── Safety override: keyword logic always wins for priority ──
        # If keywords say High but AI says Medium/Low → use High
        if keyword_priority == 'High':
            ai_result['priority'] = 'High'
        elif keyword_priority == 'Medium' and ai_result.get('priority') == 'Low':
            ai_result['priority'] = 'Medium'

        print(f"✅ Gemini AI result: {ai_result}")
        return ai_result

    except Exception as e:
        print(f"⚠️ Gemini failed, using keyword detection: {e}")
        # Fallback to pure keyword detection
        result = {
            "category": keyword_category,
            "priority": keyword_priority,
            "summary": generate_summary(title, description, keyword_category, keyword_priority)
        }
        print(f"✅ Keyword result: {result}")
        return result
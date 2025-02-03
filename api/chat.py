import requests
import random
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Directly add your Gemini API Key here
GEMINI_API_KEY = "AIzaSyD1UlQoQhP_5gzdKpX1qinKRhNieZvd6O0"  # Replace this with your actual API key
GEMINI_API_URL = "https://gemini.example.com/api/v1/ask"  # Replace with your actual Gemini API endpoint

# Store conversation history (this is just for session-based history)
user_history = {}

# Predefined error messages for the girlfriend personality
girlfriend_error_msgs = [
    "Aww, kuch galat ho gaya! 😢",
    "Hehe, thoda mistake ho gaya! 💖",
    "Oopsie, thoda confused ho gayi main! Hihi 😅",
    "Arre, kuch galat ho gaya! Phir se try karte hain? 💕",
    "Aww, galat ho gaya! Tumhe bata nahi paayi! 😘"
]

# Keywords for personality detection
girlfriend_keywords = ['love', 'baby', 'how are you', 'feel', 'miss', 'heart', 'affection', 'sweet', 'hug', 'kiss', 'cute']
bestfriend_keywords = ['what', 'how', 'lol', 'yo', 'buddy', 'mate', 'bro', 'haha', 'hey', 'fun']

def detect_personality(message):
    """Automatically detect the personality based on the user's message."""
    message_lower = message.lower()

    if any(keyword in message_lower for keyword in girlfriend_keywords):
        return "girlfriend"
    elif any(keyword in message_lower for keyword in bestfriend_keywords):
        return "bestfriend"
    
    return "bestfriend"

def get_personality_error(personality):
    """Returns a random error message based on the personality."""
    if personality == "girlfriend":
        return random.choice(girlfriend_error_msgs)
    return "Aww, kuch galat ho gaya! 😢"

def gemini_api_request(message):
    """Send the user's message to the Gemini API for response generation."""
    payload = {
        "message": message,
        "api_key": GEMINI_API_KEY
    }
    response = requests.post(GEMINI_API_URL, json=payload)
    
    if response.status_code == 200:
        return response.json().get('response', 'Sorry, I didn\'t get that.')
    else:
        return "Oops! Something went wrong. 😅"

@app.route('/chat', methods=['POST'])
def chat():
    """Endpoint to handle user messages and provide responses."""
    data = request.json
    user_id = data.get('user_id')
    message = data.get('message')

    if not user_id or not message:
        return jsonify({"error": "User ID and message are required."}), 400

    personality = detect_personality(message)

    if user_id not in user_history:
        user_history[user_id] = []

    user_history[user_id].append({"role": "user", "content": message})

    gemini_response = gemini_api_request(message)

    if "error" in gemini_response.lower():
        gemini_response = get_personality_error(personality)

    if personality == "girlfriend":
        gemini_response = "Hehe! " + gemini_response + " 💕✨"
    elif personality == "bestfriend":
        gemini_response = "Yaar, " + gemini_response + " 😂"

    user_history[user_id].append({"role": "ai", "content": gemini_response})

    return jsonify({"response": gemini_response})

if __name__ == '__main__':
    app.run(debug=True)
    

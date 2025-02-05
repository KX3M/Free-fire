from fastapi import FastAPI, Query
from transformers import pipeline
from langdetect import detect

app = FastAPI()

# AI Model Load kar rahe hain (Mistral-7B ya koi bhi Open-Source LLM)
generator = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.1", device_map="auto")

# Conversation History Store (User-specific, kisi bhi ID ke liye)
conversation_history = {}

@app.get("/ai")
def generate_ai_response(text: str, conversationId: str = Query(None), model: str = "mistral"):
    try:
        # Detecting the language
        lang = detect(text)  
        
        # Setting prefix based on language
        if lang in ["hi", "ur", "mr", "bn"]:  
            prefix = ""  # Empty for Hinglish as per your requirement
        else:
            prefix = ""  # Empty for English as per your requirement
        
        # Retrieve the last conversation history (if exists)
        if conversationId in conversation_history:
            history = conversation_history[conversationId]
        else:
            history = []

        # Add the current user message to history
        history.append(f"User: {text}")
        
        # Generate the AI response based on the entire conversation history
        full_context = " ".join(history)
        response = generator(full_context, max_length=200, num_return_sequences=1)
        
        # Store the new conversation history
        conversation_history[conversationId] = history + [f"AI: {response[0]['generated_text']}"]
        
        # Return AI response
        return {"conversationId": conversationId, "response": response[0]["generated_text"]}
    
    except Exception as e:
        return {"error": "Failed to generate response", "details": str(e)}
        

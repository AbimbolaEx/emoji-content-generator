from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
import os
import groq  
import requests

# Load environment variables from .env file
load_dotenv()


# Retrieve the API key from the environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Emoji Content Generator!"}

# Define available models
AVAILABLE_MODELS = [
    "llama-3.1-8b-instant",
    "llama-3.1-70b-versatile",
    "llama-3.1-405b-reasoning",
    "mixtral-8x7b-32768",
    # Add more models as needed
]

class Message(BaseModel):
    question: str
    model: str  # Updated to include model

class ContentRequest(BaseModel):
    emojis: List[str]
    model: str  # Updated to include model

class ContentResponse(BaseModel):
    generated_content: str

@app.get("/models")
async def get_models():
    return {"available_models": AVAILABLE_MODELS}

@app.post("/chat")
async def generate_chat(msg: Message):
    query = msg.question
    model = msg.model
    if model not in AVAILABLE_MODELS:
        return {"error": f"Model '{model}' is not supported."}
    try:
        groq_client = groq.Client(api_key=GROQ_API_KEY)
        response = groq_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": query},
            ],
            temperature=0.7
        )
        content = response.choices[0].message.content
        return {"response": content}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

@app.post("/generate-content", response_model=ContentResponse)
async def generate_content(request: ContentRequest):
    emojis = request.emojis
    model = request.model
    if model not in AVAILABLE_MODELS:
        return {"error": f"Model '{model}' is not supported."}
    query = f"Generate content based on these emojis: {' '.join(emojis)}"
    try:
        groq_client = groq.Client(api_key=GROQ_API_KEY)
        response = groq_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": query},
            ],
            temperature=0.7
        )
        generated_content = response.choices[0].message.content
        return ContentResponse(generated_content=generated_content)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
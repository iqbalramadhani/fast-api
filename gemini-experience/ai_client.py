import os
from dotenv import load_dotenv
from google import genai
from fastapi import HTTPException

load_dotenv()

gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def ask_gemini(prompt: str) -> str:
    try:    
        response = gemini_client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=prompt
        )
        
        return response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while communicating with Gemini API: {str(e)}")
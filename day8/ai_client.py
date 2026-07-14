import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from fastapi import HTTPException

load_dotenv()

gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

DEFAULT_SYSTEM_PROMPT = """Kamu adalah asisten produktivitas untuk aplikasi Todo List. Jawab dalam Bahasa Indonesia yang santai tapi profesional, maksimal 3 kalimat. Kalau ditanya diluar topik todo/produktivitas, arahkan balik dengan sopan."""

def ask_gemini(
    prompt: str,
    system_instruction: str = DEFAULT_SYSTEM_PROMPT,
    temperature: float = 0.7,
    max_output_tokens: int = 500
):
    try:
        response = gemini_client.models.generate_content(
            model="gemini-flash-lite-latest",
            content=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=temperature,
                max_output_tokens=max_output_tokens
            )
        )

        return response.text
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"Gagal menghubungi AI service : {str(e)}"
        )

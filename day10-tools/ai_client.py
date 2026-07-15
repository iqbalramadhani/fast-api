import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from fastapi import HTTPException
from ai_tools import create_todo_tools, list_pending_todos_tool

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
            contents=prompt,
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

def ask_gemini_stream(prompt:str,system_instruction:str=DEFAULT_SYSTEM_PROMPT):
    response = gemini_client.models.generate_content_stream(
        model="gemini-flash-lite-latest",
        contents=prompt,
        # config=types.GenerateContentConfig(
        #     system_instruction=system_instruction
        # )
    )

    for chunk in response:
        if chunk.text:
            yield chunk.text


def ask_gemini_with_tools(promp: str) -> str:
    try:
        response = gemini_client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=promp,
            config=types.GenerateContentConfig(
                system_instruction=DEFAULT_SYSTEM_PROMPT,
                tools=[create_todo_tools,list_pending_todos_tool]
            )
        )

        return response.text
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Gagal menghubungi AI service : {str(e)}")

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from fastapi import HTTPException
from ai_tools import create_todo_tools, list_pending_todos_tool, list_all_todos_tool, update_todo_status_tool

load_dotenv()

gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

DEFAULT_SYSTEM_PROMPT = """Kamu adalah asisten produktivitas untuk aplikasi Todo List.
Aturan : 
1. Jawab dalam Bahasa Indonesia yang santai tapi profesional, 
2. Untuk pertanyaan umum, jawab singkat maksimal 3 kalimat.
3. Tapi kalau user meminta melihat daftar/list todo, WAJIB tampilkan semua item secara lengkap dalam
   format bullet point, jangan diringkas
4. Kalau ditanya diluar topik todo/produktivitas, arahkan balik dengan sopan."""

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

# simpan hisotry percakapan per session_id
chat_sessions: dict[str, list] = {}

def get_or_create_chat(session_id: str):
    if session_id not in chat_sessions:
        chat_sessions[session_id] = gemini_client.chats.create(
            model="gemini-flash-lite-latest",
            config=types.GenerateContentConfig(
                system_instruction=DEFAULT_SYSTEM_PROMPT,
                tools=[
                    create_todo_tools,
                    list_pending_todos_tool,
                    list_all_todos_tool,
                    update_todo_status_tool
                ]
            )
        )
    
    return chat_sessions[session_id]

def chat_with_assistant(session_id:str, message:str)-> str:
    try:
        chat = get_or_create_chat(session_id)
        response = chat.send_message(message)
        return response.text
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Gagal menghubungi AI service: {str(e)}")
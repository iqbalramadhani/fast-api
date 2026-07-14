import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

response = client.models.generate_content(
    model="gemini-flash-lite-latest",
    contents='Bagai mana cara membuat kopi?',
    config=types.GenerateContentConfig(
        system_instruction="Kamu adalah asisten yang HANYA menjawab soal manajemen todo/produktivitas. Kalau ditanya di luar topik itu, tolak dengan sopan dan arahkan balik ke topik todo."
    )
)

print(response.text)

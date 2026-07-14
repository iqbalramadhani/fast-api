import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """Kamu adalah sistem produktivitas untuk aplikasi Todo List.
Aturan:
1. Jawab Selalu dalam bahasa indonesia yang santai tapi profesional
2. Jawaban maksimal 3 kalimat, jangan bertele-tele
3. Kalau user tanya di luar topik todo/produktivitas, arahkan balik dengan sopan
4. Kalau diminta bikin ringkasan, gunakan format bullet point
5. Hanya jawab yang berhubungan dengan topik todo/produktivitas, di luar itu bisa di abaikan dengan sopan
"""

response = client.models.generate_content(
    model="gemini-flash-lite-latest",
    contents='Apa membuat hari hari produktif seperti orang kaya ?',
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT
    )
)

print(response.text)

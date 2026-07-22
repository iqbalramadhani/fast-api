import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

# 1. Definisakan fungsi python biasa
def get_weather(city:str)->str:
    """Dapetin info cuaca untuk sebuah kota"""
    # ini dummy, di real case manggil API cuaca beneran
    return f"Cuaca di {city} adalah cerah, 28 C"

def create_reminder(title: str, date: str) -> str:
    """Membuat pengingat baru dengan judul dan tanggal tertentu. 
    Gunakan ini kalau user minta dibuatkan reminder/pengingat."""
    return f"Reminder '{title}' dibuat untuk tanggal {date}"

def delete_reminder(reminder_id: int) -> str:
    """Menghapus reminder berdasarkan ID-nya."""
    return f"Reminder {reminder_id} berhasil dihapus"


# 2. Kasih tau gemini fungsi ini
response = client.models.generate_content(
    model="gemini-flash-lite-latest",
    contents="Ingetin saya besok beli obat",
    config=types.GenerateContentConfig(
        tools=[get_weather,create_reminder,delete_reminder]
    )
)

print(response.text)
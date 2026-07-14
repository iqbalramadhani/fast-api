# max_output_tokens

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

prompt = "Jelasin sejarah lengkap internet dari awal sampai akhir"

response = client.models.generate_content(
    model="gemini-flash-lite-latest",
    contents=prompt,
    config=types.GenerateContentConfig(
        max_output_tokens=50
    )
)

print(response.text)
print("Finish reason:",response.candidates[0].finish_reason)
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

response = client.models.generate_content_stream(
    model="gemini-flash-lite-latest",
    contents="ceriitakan tentang sejarah internet"
)

for chunk in response:
    print(chunk.text, end="", flush=True)
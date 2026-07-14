import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

prompt = "Kasih 1 tips produktivitas singkat"

for temp in [0.0,1.0,2.0]:
    response = client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temp
        )
    )

    print(f"Temperature {temp}: {response.text}")
    print("------")

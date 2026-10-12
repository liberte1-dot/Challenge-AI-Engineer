import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key = os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

reponse = client.chat.completions.create(
    model="gemini-3.8-flash",
    messages=[{"role": "user", "content": "Dis bonjour en une phrase."}],
)

print(reponse.choices[0].message.content)
print(reponse.usage)
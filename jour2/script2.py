import os
import tiktoken
from dotenv import load_dotenv
from openai import OpenAI

from dotenv import find_dotenv
print("Fichier .env trouvé :", find_dotenv() or "AUCUN")
print("Clé chargée :", bool(os.getenv("GEMINI_API_KEY")))

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
enc = tiktoken.get_encoding("cl100k_base")

textes = [
    "Hello, how are you?",
    "Bonjour, comment allez-vous ?",
    "Explique en détail le fonctionnement d'un tokenizer BPE.",
    "def add(a, b): return a + b",
]

print(f"{'tiktoken':>9} | {'Gemini':>7} | texte")
for texte in textes:
    local = len(enc.encode(texte))
    rep = client.chat.completions.create(
        model="gemini-3.6-flash",
        messages=[{"role": "user", "content": texte}],
        max_tokens=1000,
    )
    reel = rep.usage.prompt_tokens
    print(f"{local:>9} | {reel:>7} | {texte[:45]}")
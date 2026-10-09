import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI

# On charge la cle d'API contenu dans le fichier .env
load_dotenv()

# On utilise cette adresse qui va servir de base pour retrouver les modeles d'IA
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

class LLMClient :
    def __init__(self, model="gemini-3.6-flash", max_retries=3, timeout=300.0):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY introuvable : vérifie ton fichier .env")
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=GEMINI_BASE_URL,
            timeout=timeout,
            max_retries=0
        )
        self.model = model
        self.max_retries = max_retries

    async def complete(
            self,
            prompt,
            system="Tu es un assistant utile.",
            temperature=0.7,
            presence_penalty=0.0,
            frequency_penalty=0.0,
            max_tokens=1000
    ):
        messages = [
            {"role":"system", "content":system},
            {"role":"user", "content":prompt},
        ]
        params = {
            "model" : self.model,
            "messages" : messages,
            "temperature" : temperature,
            "max_tokens":max_tokens
        }
        # On n'envoie les pénalités que si elles sont utilisées
        if presence_penalty:
            params["presence_penalty"] = presence_penalty
        if frequency_penalty:
            params["frequency_penalty"] = frequency_penalty

        reponse = await self.client.chat.completions.create(**params)
        return reponse.choices[0].message.content


async def main():
    llm = LLMClient()
    texte = await llm.complete("Dis bonjour en une phrase.", temperature=0)
    print(texte)

if __name__ == "__main__" :
    asyncio.run(main())
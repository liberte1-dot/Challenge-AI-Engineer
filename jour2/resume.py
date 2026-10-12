import os
from dotenv import load_dotenv
from openai import OpenAI
from fenetre import compter

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
MODELE = "gemini-3.6-flash"


def resumer(anciens):
    """Demande à Gemini de résumer une liste de messages."""
    transcription = "\n".join(f"{m['role']}: {m['content']}" for m in anciens)
    rep = client.chat.completions.create(
        model=MODELE,
        messages=[
            {
                "role": "system",
                "content": "Tu résumes des conversations. Garde les faits "
                           "importants (noms, lieux, préférences, décisions). "
                           "Réponds en 2 phrases maximum.",
            },
            {"role": "user", "content": transcription},
        ],
        temperature=0,
        max_tokens=1000,
    )
    return rep.choices[0].message.content


def fenetre_avec_resume(messages, garder=4):
    systeme = [m for m in messages if m["role"] == "system"]
    autres = [m for m in messages if m["role"] != "system"]

    if len(autres) <= garder:
        return messages          # rien à résumer

    anciens = autres[:-garder]
    recents = autres[-garder:]

    resume = resumer(anciens)
    note = {
        "role": "system",
        "content": f"Résumé de la conversation précédente : {resume}",
    }
    return systeme + [note] + recents


if __name__ == "__main__":
    conversation = [
        {"role": "system", "content": "Tu es un assistant concis."},
        {"role": "user", "content": "Je m'appelle Sam et j'habite à Lyon."},
        {"role": "assistant", "content": "Enchanté Sam !"},
        {"role": "user", "content": "Quelle est la capitale de l'Italie ?"},
        {"role": "assistant", "content": "Rome."},
        {"role": "user", "content": "Et celle de l'Espagne ?"},
        {"role": "assistant", "content": "Madrid."},
        {"role": "user", "content": "Et celle du Portugal ?"},
    ]

    reduite = fenetre_avec_resume(conversation, garder=4)

    print(f"Avant : {len(conversation)} messages, {compter(conversation)} tokens")
    print(f"Après : {len(reduite)} messages, {compter(reduite)} tokens\n")
    for m in reduite:
        print(f"[{m['role']}] {m['content']}")
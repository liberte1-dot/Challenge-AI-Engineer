import tiktoken

enc = tiktoken.get_encoding("cl100k_base")


def compter(messages):
    """Nombre approximatif de tokens d'une liste de messages."""
    return sum(len(enc.encode(m["content"])) for m in messages)


def fenetre_glissante(messages, max_messages=4):
    """Garde le message système + les derniers messages."""
    systeme = [m for m in messages if m["role"] == "system"]
    autres = [m for m in messages if m["role"] != "system"]
    return systeme + autres[-max_messages:]


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

    reduite = fenetre_glissante(conversation, max_messages=4)

    print(f"Avant : {len(conversation)} messages, {compter(conversation)} tokens")
    print(f"Après : {len(reduite)} messages, {compter(reduite)} tokens\n")
    for m in reduite:
        print(f"[{m['role']}] {m['content']}")
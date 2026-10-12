from fenetre import compter


def tronquer(messages, max_tokens):
    """Garde les consignes système + les messages les plus récents
    qui tiennent dans la limite de tokens."""
    systeme = [m for m in messages if m["role"] == "system"]
    autres = [m for m in messages if m["role"] != "system"]

    budget = max_tokens - compter(systeme)
    if budget <= 0:
        raise ValueError("Les consignes système dépassent déjà la limite.")

    gardes = []
    for m in reversed(autres):       # on part du plus récent
        cout = compter([m])
        if cout > budget:
            break                    # la valise est pleine, on s'arrête
        gardes.append(m)
        budget = budget - cout

    gardes.reverse()                 # on remet dans l'ordre normal
    return systeme + gardes


def message(role, mot, n):
    """Fabrique un message long en répétant un mot n fois."""
    return {"role": role, "content": (mot + " ") * n}


if __name__ == "__main__":
    conversation = [
        {"role": "system", "content": "Tu es un assistant concis."},
        message("user", "ancien", 60),
        message("assistant", "reponse", 60),
        message("user", "milieu", 40),
        message("assistant", "reponse", 40),
        message("user", "recent", 20),
    ]

    reduite = tronquer(conversation, max_tokens=150)

    print(f"Avant : {len(conversation)} messages, {compter(conversation)} tokens")
    print(f"Après : {len(reduite)} messages, {compter(reduite)} tokens\n")
    for m in reduite:
        print(f"[{m['role']}] {m['content'][:30]}...")
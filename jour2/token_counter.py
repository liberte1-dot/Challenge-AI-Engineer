"""token_counter.py : compter les tokens et adapter le contexte (jour 2)."""
import tiktoken

_ENC = tiktoken.get_encoding("cl100k_base")

# Prix en dollars par million de tokens.
# À remplir avec les prix lus sur la page officielle de Google.
PRIX = {
    "gemini-3.6-flash": {"entree": 0.0, "sortie": 0.0},
}


# ---------- 1. Compter ----------
def compter_texte(texte):
    """Nombre de tokens d'un texte (estimation avec tiktoken)."""
    return len(_ENC.encode(texte))


def compter_messages(messages):
    """Nombre de tokens d'une liste de messages."""
    return sum(compter_texte(m["content"]) for m in messages)


# ---------- 2. Coût ----------
def estimer_cout(modele, tokens_entree, tokens_sortie):
    """Coût estimé en dollars d'une requête."""
    if modele not in PRIX:
        raise ValueError(f"Modèle inconnu : {modele}. Ajoute-le dans PRIX.")
    p = PRIX[modele]
    return (tokens_entree / 1_000_000 * p["entree"]
            + tokens_sortie / 1_000_000 * p["sortie"])


# ---------- 3. Adapter le contexte ----------
def _separer(messages):
    systeme = [m for m in messages if m["role"] == "system"]
    autres = [m for m in messages if m["role"] != "system"]
    return systeme, autres


def fenetre_glissante(messages, max_messages=4):
    """Garde les consignes système + les derniers messages."""
    systeme, autres = _separer(messages)
    if max_messages <= 0:
        return systeme
    return systeme + autres[-max_messages:]


def tronquer(messages, max_tokens):
    """Garde les consignes système + les messages les plus récents
    qui tiennent dans la limite de tokens."""
    systeme, autres = _separer(messages)

    budget = max_tokens - compter_messages(systeme)
    if budget <= 0:
        raise ValueError("Les consignes système dépassent déjà la limite.")

    gardes = []
    for m in reversed(autres):
        cout = compter_messages([m])
        if cout > budget:
            break
        gardes.append(m)
        budget -= cout

    gardes.reverse()
    return systeme + gardes


# ---------- Démonstration et tests ----------
if __name__ == "__main__":
    conversation = [
        {"role": "system", "content": "Tu es un assistant concis."},
        {"role": "user", "content": "ancien " * 60},
        {"role": "assistant", "content": "reponse " * 60},
        {"role": "user", "content": "milieu " * 40},
        {"role": "assistant", "content": "reponse " * 40},
        {"role": "user", "content": "recent " * 20},
    ]

    total = compter_messages(conversation)
    print(f"Conversation complète : {len(conversation)} messages, {total} tokens")

    glissee = fenetre_glissante(conversation, max_messages=2)
    print(f"Fenêtre glissante (2) : {len(glissee)} messages, "
          f"{compter_messages(glissee)} tokens")

    tronquee = tronquer(conversation, max_tokens=150)
    print(f"Troncature (150)      : {len(tronquee)} messages, "
          f"{compter_messages(tronquee)} tokens")

    print(f"Coût estimé de la conversation complète : "
          f"{estimer_cout('gemini-3.6-flash', total, 100):.6f} $")

    # Tests automatiques : si une ligne est fausse, Python s'arrête avec une erreur
    assert glissee[0]["role"] == "system"
    assert len(glissee) == 3                      # 1 système + 2 messages
    assert tronquee[0]["role"] == "system"
    assert compter_messages(tronquee) <= 150
    print("\nTous les tests sont passés.")
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")


textes = [
    "Hello, how are you?",
    "Bonjour, comment allez-vous ?",
    "Internationalisation",
    "def add(a, b): return a + b",
    "2026",
]

for texte in textes:
    tokens = enc.encode(texte)
    morceaux = [enc.decode([t]) for t in tokens]
    print(f"{texte!r}")
    print(f"  mots/caractères : {len(texte)} caractères")
    print(f"  tokens          : {len(tokens)}")
    print(f"  découpage       : {morceaux}\n")
# Jour 2 : Tokenization, coût et gestion du contexte

Deuxième jour du programme **« Ingénieur IA : LLM & Agents »** (semaine 1).

## Objectif

Comprendre comment un LLM « lit » un texte (en tokens), estimer ce que coûte une requête, et gérer une conversation qui devient trop longue pour la fenêtre de contexte.

**Livrable :** `token_counter.py`, un module qui compte les tokens, estime le coût et adapte le contexte.

## Structure du dossier

```
jour2/
├── .env                 # clé API réelle (jamais versionnée)
├── script2.py           # comparaison tiktoken vs compte réel de Gemini
├── cost.py              # estimation du coût d'une requête
├── fenetre.py           # fenêtre glissante
├── resume.py            # résumé automatique des anciens messages
├── tronquer.py          # troncature dynamique par nombre de tokens
├── token_counter.py     # module final (livrable du jour)
└── README.md
```

Le fichier `.env` n'est pas poussé sur GitHub : le `.env.example` du projet sert de modèle.

## Ce que j'ai fait, étape par étape

### 1. Découvrir les tokens avec `tiktoken`
Un LLM ne lit pas des mots mais des **tokens** (morceaux de mots). J'ai chargé l'encodage `cl100k_base` et observé comment des phrases en français, en anglais, du code et des nombres sont découpés.

```python
enc = tiktoken.get_encoding("cl100k_base")
```

`tiktoken` est le tokenizer d'OpenAI, pas celui de Gemini : ses chiffres sont donc des **estimations** pour Gemini.

### 2. Comparer avec le compte réel de Gemini
J'ai comparé mon compte local au champ `usage.prompt_tokens` renvoyé par Gemini (modèle `gemini-3.6-flash`) :

| Texte | tiktoken | Gemini |
|---|---|---|
| `Hello, how are you?` | 6 | 7 |
| `Bonjour, comment allez-vous ?` | 7 | 8 |
| `Explique en détail le fonctionnement d'un tokenizer BPE.` | 14 | 14 |
| `def add(a, b): return a + b` | 10 | 12 |

**Conclusion :** les écarts sont faibles (0 à 2 tokens) sur ces quatre exemples, donc `tiktoken` donne une bonne estimation. Pour une limite stricte ou une facture, c'est le compte de Gemini qui fait foi. Quatre phrases courtes ne suffisent pas pour généraliser.

### 3. Estimer le coût (`cost.py`)
Le coût d'une requête = tokens d'entrée × prix d'entrée + tokens de sortie × prix de sortie, avec des prix exprimés **par million de tokens**.

> Statut : *les prix de la table `PRIX` restent à remplir avec les tarifs de la page officielle de Google.* Sur l'offre gratuite, le coût réel est de 0 $.

Le coût en argent n'est pas le seul : latence, quotas, qualité, confidentialité des données et fiabilité comptent aussi.

### 4. Fenêtre glissante (`fenetre.py`)
Un LLM n'a pas de mémoire : on lui renvoie toute la conversation à chaque requête. La fenêtre glissante garde le **message système** et les **N derniers messages**.

**Limite :** les informations des anciens messages sont perdues (par exemple un prénom donné au début).

### 5. Résumé automatique (`resume.py`)
Les anciens messages sont envoyés à Gemini pour être résumés, puis remplacés par ce résumé, suivi des messages récents. Cela évite de perdre les faits importants.

**Limites :** un résumé fait perdre de l'information, chaque résumé coûte un appel supplémentaire, et sur une conversation très courte le gain en tokens est faible.

### 6. Troncature dynamique (`tronquer.py`)
On garde le message système, puis on ajoute les messages en partant du plus récent tant qu'ils tiennent dans un budget de tokens. Cette méthode compte des **tokens** et non des messages.

Résultat sur ma conversation de test (limite de 150 tokens) :

| | Avant | Après |
|---|---|---|
| Messages | 6 | 3 |
| Tokens | 393 | 109 |

**Limite observée :** la conversation conservée peut commencer par une réponse dont la question a été supprimée.

### 7. Assemblage (`token_counter.py`)
Regroupe en un seul module : comptage de tokens (`compter_texte`, `compter_messages`), estimation du coût (`estimer_cout`), fenêtre glissante et troncature. Le fichier contient une démonstration et quelques tests automatiques (`assert`). Le résumé automatique reste séparé dans `resume.py`, car il appelle l'API.

## Concepts clés retenus

- **Token :** brique de texte, pas forcément un mot. Un même texte peut avoir un nombre de tokens différent selon le tokenizer.
- **Fenêtre de contexte :** la quantité de texte que le modèle peut « voir » à la fois (prompt + réponse).
- **Message système :** les consignes de fond, à ne jamais supprimer lors d'une réduction du contexte.
- **Fenêtre glissante, résumé, troncature :** trois façons de réduire le contexte, avec chacune ses limites. On peut les combiner.

## Erreurs rencontrées et leçons

- `Missing credentials` : `load_dotenv()` ne trouve pas le `.env` s'il n'est ni dans le dossier du script ni dans un dossier parent. J'ai copié le `.env` dans `jour2`.
- Un diagnostic placé **avant** `load_dotenv()` affiche toujours `False`, même si la clé est bonne : l'ordre des lignes compte.
- Ne jamais coller sa clé API dans un message ou un fichier partagé.

## Lancer le code

```bash
source .venv/bin/activate
pip install tiktoken openai python-dotenv
cp .env.example .env            # puis mets ta propre clé dans .env
python token_counter.py
```

Les scripts `script2.py` et `resume.py` appellent l'API Gemini ; `token_counter.py`, `fenetre.py`, `tronquer.py` et `cost.py` fonctionnent sans appel réseau.

## Livrable du jour

`token_counter.py` : module de comptage de tokens, d'estimation de coût et d'adaptation du contexte.

## Suite

Jour 3 : prompt engineering structuré, few-shot et bibliothèque de prompts versionnée.

# Jour 1 : Prise en main des APIs LLM & architecture de requêtes

Premier jour du programme **« Ingénieur IA : LLM & Agents »** (8 semaines).

## Objectif

Apprendre à appeler un LLM depuis du code Python de façon **fiable** et **non bloquante**, et construire un client réutilisable : `llm_client.py`.

Fournisseur utilisé : **Google Gemini**, via son endpoint compatible OpenAI (gratuit, sans carte bancaire). La librairie `openai` fonctionne telle quelle, seuls trois éléments changent : la clé, le `base_url` et le nom du modèle.

## Structure du dossier

```
jour 1/
├── .env              # clé API réelle (jamais versionnée)
├── .env.example      # modèle sans clé, versionné sur GitHub
├── .gitignore        # exclut .env, .venv/, __pycache__/
├── test_appel.py     # premier appel synchrone de vérification
├── llm_client.py     # client LLM asynchrone (livrable du jour)
└── README.md
```

## Ce que j'ai fait, étape par étape

### 1. Clé API
Création d'une clé gratuite sur Google AI Studio. La clé est stockée uniquement dans `.env`.

### 2. Environnement virtuel
Création d'un environnement virtuel Python (`venv`) pour isoler les dépendances du projet.

### 3. Installation des dépendances

```bash
pip install openai langchain-openai pydantic python-dotenv
```

### 4. Sécurisation de la clé
- `.env` contient `GEMINI_API_KEY=...` (clé réelle, local uniquement).
- `.gitignore` empêche l'envoi de `.env` sur GitHub.
- `.env.example` est le fichier modèle poussé à la place de `.env` : il liste les variables attendues avec une valeur factice (`GEMINI_API_KEY=ta_cle_ici`), sans jamais contenir de vraie clé.

### 5. Premier appel de test (`test_appel.py`)
Appel synchrone simple pour vérifier que la clé, l'URL et le modèle fonctionnent.

**Erreurs rencontrées et leçons :**
- `Missing credentials` : le nom de la variable dans le code (`GEMENI_API_KEY`) ne correspondait pas à celui du `.env`, et `load_dotenv()` n'était pas appelé. Les noms doivent être identiques lettre pour lettre, et `load_dotenv()` doit s'exécuter **avant** la création du client.

### 6. Classe `LLMClient`
Regroupe la clé, le `base_url`, le modèle, le délai maximal (`timeout`) et le nombre d'essais. Si la clé est introuvable, une erreur claire est levée immédiatement.

### 7. Méthode asynchrone `complete()`
Envoie une requête avec les réglages suivants :

| Paramètre | Rôle |
|---|---|
| `prompt` | La question de l'utilisateur |
| `system` | Le rôle et les consignes de fond du modèle |
| `temperature` | Créativité : 0 = stable, valeurs élevées = plus varié |
| `presence_penalty` | Pénalise les sujets déjà apparus |
| `frequency_penalty` | Pénalise les mots répétés |
| `max_tokens` | Longueur maximale de la réponse |

**Points notés :**
- Les pénalités ne sont envoyées que si elles sont non nulles, car Gemini ne les traite pas forcément comme OpenAI. À tester.
- Avec Gemini 2.5, une partie de `max_tokens` peut servir à la « réflexion » interne : une valeur trop basse peut donner une réponse vide ou tronquée.

### 8. Gestion des erreurs et réessais
Erreur `503 UNAVAILABLE` rencontrée (serveur surchargé), c'est le cas que cette étape doit gérer.

Principe : **backoff exponentiel** (attente de 1 s, 2 s, 4 s...) pour les erreurs temporaires (429, 5xx, connexion, timeout). Les erreurs d'authentification ne sont pas réessayées. Les échecs finaux sont convertis en une erreur lisible (`LLMError`).

> Statut : *à compléter une fois l'étape validée.*

### 9. Test en parallèle (`asyncio.gather`)
> Statut : *à venir.* Lancer 3 requêtes en parallèle et vérifier que le temps total est proche de celui d'une seule requête.

## Concepts clés retenus

- **`base_url`** : l'adresse du serveur vers lequel la librairie envoie les requêtes. Changer de fournisseur compatible OpenAI ne demande pas de réécrire le code.
- **`async` / `await`** : permettent de lancer plusieurs appels sans attendre que chacun soit terminé.
- **Backoff exponentiel** : espacer les tentatives pour laisser le serveur récupérer.

## Lancer le projet

```bash
python -m venv .venv
source .venv/bin/activate          # Windows : .venv\Scripts\activate
pip install openai langchain-openai pydantic python-dotenv
cp .env.example .env               # puis remplace la valeur par ta vraie clé
python llm_client.py
```

## Livrable du jour

`llm_client.py` : client LLM asynchrone avec paramètres de génération configurables et gestion des erreurs d'API.

## Suite

Jour 2 : tokenization, comptage exact des tokens et gestion de la fenêtre de contexte.

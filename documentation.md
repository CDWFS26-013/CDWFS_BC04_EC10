# Distance Calculator

Application web Flask de calcul de distance euclidienne entre deux points d'un plan à 2 dimensions, basée sur le théorème de Pythagore.

## Formule utilisée

`distance(AB) = sqrt((Bx - Ax)² + (By - Ay)²)`

Exemple : A(2, 5) et B(1, 6) → distance = sqrt((-1)² + (1)²) = sqrt(2) ≈ 1.414

---

## Prérequis

- Python 3.10+
- pip

---

## Installation

```bash
# Cloner le projet
git clone <url-du-projet>
cd CDWFS_BC04_EC10

# Créer un environnement virtuel
python -m venv .venv

# Activer l'environnement virtuel
# Windows :
.venv\Scripts\activate
# Linux/macOS :
source .venv/bin/activate

# Installer les dépendances
pip install flask pytest pytest-cov flake8
```

---

## Lancer l'application

```bash
flask --app app run
```

L'application est accessible à l'adresse : http://127.0.0.1:5000

---

## Utilisation de l'interface web

1. Ouvrir http://127.0.0.1:5000 dans un navigateur
2. Saisir les coordonnées du point A dans le premier champ (format : `x,y` — exemple : `2,5`)
3. Saisir les coordonnées du point B dans le second champ (format : `x,y` — exemple : `1,6`)
4. Cliquer sur **Soumettre**
5. La distance calculée s'affiche sur la page

---

## Utilisation de l'API

### Calculer une distance

```
POST /api/distance
Content-Type: application/json

{
  "start_point": "2,5",
  "end_point": "1,6"
}
```

Réponse :
```json
{
  "requested_at": "2026-06-17T10:00:00.000000",
  "result_distance": 1.4142135623730951,
  "start_point": [2, 5],
  "end_point": [1, 6]
}
```

### Lister les calculs effectués

```
GET /api/distances
```

Retourne la liste de tous les calculs effectués depuis le démarrage du serveur.

---

## Lancer les tests

```bash
pytest test_app.py -v
```

---

## Mesurer la couverture de tests

```bash
# Rapport dans le terminal
pytest --cov=app --cov-report=term-missing

# Rapport HTML (ouvrir htmlcov/index.html)
pytest --cov=app --cov-report=html
```

---

## Analyse statique (dette technique)

```bash
# Analyse de style et erreurs
flake8 app.py

# Analyse qualité
pylint app.py
```

---

## Structure du projet

```
CDWFS_BC04_EC10/
├── app.py              # Application Flask principale
├── test_app.py         # Tests automatisés (pytest)
├── documentation.md    # Documentation
├── openapi.yaml        # Documentation API au format OpenAPI 3.0
├── api_tests.http      # Fichier de tests HTTP (VS Code REST Client)
├── questionnaire.md    # Réponses aux questions du sujet
└── templates/
    └── index.html      # Interface web HTML
```

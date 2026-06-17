# Questionnaire — Réponses

## 1. Quelle était la dette technique en début de projet ? Comment l'avez-vous mesurée ?

La dette technique a été mesurée avec les outils d'analyse statique **flake8** et **pylint**.

Problèmes identifiés dans `app.py` :

- **Nommage non conforme PEP8** : `eNd` (ligne 16) et `EndPoint` (ligne 20) mélangent majuscules et minuscules de façon incohérente
- **Variable inutile** : ligne 54, `startPoint = request.json['start_point']` est immédiatement écrasée à la ligne 55, la première assignation ne sert à rien
- **Code mort (unreachable code)** : dans `already_calculated()`, le `print()` se trouve **après** le `return` (ligne 50) et ne s'exécutera jamais
- **Duplication de code** : dans `html_calculate()`, le dictionnaire de résultat est construit deux fois (lignes 21–26 et 27–32) avec les mêmes données
- **Nom de fonction non conforme** : `Calculate()` devrait être `calculate()` selon PEP8
- **Méthodes HTTP inappropriées** : `/api/distance` accepte GET, POST et PUT alors que seul POST est logique ici
- **Aucune gestion des erreurs** : aucun `try/except` — si l'utilisateur envoie "abc,xyz", le serveur plante
- **Formatage irrégulier** : indentation et espaces incohérents dans la construction des dictionnaires résultats

Score pylint initial estimé : **~3/10**

---

## 2. Quelle était la couverture en début de projet ? Comment l'avez-vous mesurée ?

La couverture de tests était de **0 %**.

Il n'existe aucun fichier de test dans le projet initial (aucun `test_*.py` ou `*_test.py`).

Mesure effectuée avec la commande :
```bash
pytest --cov=app --cov-report=term
```
Résultat : aucun test découvert, couverture = 0 %.

---

## 3. Quelle est la dette technique après vos modifications ? Qu'en dites-vous ?

Après modifications, la dette technique a été fortement réduite :

- Variables renommées conformément à PEP8 (`end_point`, `start_point`)
- Code mort (`print` après `return`) supprimé
- Première assignation inutile de `startPoint` supprimée
- Duplication du dictionnaire résultat éliminée (construction une seule fois)
- Gestion des erreurs ajoutée (`try/except`) sur les entrées utilisateur
- Méthodes HTTP corrigées sur la route `/api/distance` (POST uniquement)

Score pylint après modifications : **~8.5/10**

La dette résiduelle concerne principalement l'architecture : le stockage des distances dans une liste en mémoire (`distances = list()`) signifie que toutes les données sont perdues au redémarrage du serveur. Une base de données serait nécessaire pour un usage en production.

---

## 4. Quelle est la couverture en fin de projet après vos modifications ? Qu'en dites-vous ?

Après ajout des tests, la couverture atteint **~90 %** des lignes de code.

Les tests couvrent :
- Route GET `/` : affichage du formulaire vide
- Route POST `/` avec des coordonnées valides (ex: `2,5` et `1,6`)
- Route POST `/` avec des coordonnées invalides (texte non numérique)
- Route GET `/api/distances` : récupération de la liste
- Route POST `/api/distance` avec un JSON valide
- Route POST `/api/distance` avec un JSON invalide ou manquant

Commande de mesure :
```bash
pytest --cov=app --cov-report=term-missing
```

Les ~10 % restants correspondent à des branches d'erreur très peu probables. Une couverture de 90 % est un résultat satisfaisant pour ce type d'application.

---

## 5. État des lieux — Écart entre les attentes et l'état actuel

| Attente du contexte | État initial du projet | Écart |
|---|---|---|
| Application de calcul de distance fonctionnelle | Fonctionnelle mais fragile (pas de gestion d'erreurs) | Partiel |
| Tests adaptés à l'interaction utilisateur | **0 test** | **Critique** |
| Couverture exhaustive | **0 %** | **Critique** |
| API REST correcte | Partiellement conforme (méthodes HTTP incorrectes, pas de sauvegarde des résultats via API) | Moyen |
| Code de qualité / lisible | Multiples violations PEP8, code mort, duplication | Fort |
| Documentation technique | **Absente** | **Critique** |

L'écart le plus grave est l'absence totale de tests et de documentation. L'application est fonctionnelle dans le cas nominal, mais un seul appel avec des données incorrectes provoque une erreur 500 non gérée.

---

## 6. Méthode de travail — Schéma de branches

Conformément aux consignes du sujet, **tous les commits ont été réalisés directement sur la branche `main`**, sans branche de travail distincte.

```
main
 │
 ├── a972afc  Git init (état initial reçu du développeur principal)
 │
 ├── [commit] Tests fixed          ← ajout des tests automatisés
 │
 ├── [commit] Documentation        ← rédaction du README
 │
 ├── [commit] OpenAPI              ← documentation de l'API au format OpenAPI
 │
 ├── [commit] SAST/DAST fixed      ← configuration flake8 / pytest-cov
 │
 └── [commit] API                  ← fichiers de test de l'API (collection Postman / fichier HTTP)
```

Si un workflow en branches avait été utilisé, il aurait suivi ce modèle :
```
main ──────────────────────────────────────────► (production)
        │                        │
        └─► feature/tests ──────►┘  (merge via Pull Request)
        └─► feature/docs  ──────►┘
```

---

## 7. L'API répond-elle aux exigences d'une architecture REST ?

**Non, pas entièrement.** L'API présente plusieurs non-conformités REST.

**Problèmes identifiés :**

- **Méthodes HTTP incorrectes** : `/api/distance` accepte `GET`, `POST` et `PUT`. En REST, `GET` doit être idempotent et ne jamais modifier l'état du serveur. `PUT` sert à remplacer une ressource existante. Ici seul `POST` est justifié (création d'un nouveau calcul).
- **Incohérence de comportement** : la route HTML `POST /` sauvegarde le résultat dans `distances`, mais `POST /api/distance` ne le fait pas. Le même calcul donne des effets de bord différents selon la route utilisée.
- **Route `/api` inutile** : retourne `{}` sans aucune information. Une API REST bien conçue retournerait au minimum les routes disponibles (HATEOAS) ou un objet d'information.
- **Codes de statut HTTP absents** : l'API retourne toujours 200. Elle devrait retourner 201 (Created) pour un calcul créé, 400 (Bad Request) pour une entrée invalide, 422 pour des données mal formées.
- **Pas de versioning** : l'URL devrait être `/api/v1/distance` pour permettre des évolutions sans casser les clients existants.

**Points conformes :**
- Utilisation du format JSON pour les échanges
- Nommage des ressources en minuscules
- Route dédiée pour lister les résultats (`/api/distances`)

---

## 8. Quel framework de tests a été utilisé par le développeur principal ?

**Aucun.** Le développeur principal n'a utilisé aucun framework de tests. Il n'existe aucun fichier de test dans le projet initial.

Pour un projet Flask en Python, les frameworks adaptés sont :
- **pytest** (recommandé) avec le client de test Flask via `app.test_client()`
- **unittest** (bibliothèque standard Python, sans installation supplémentaire)

---

## 9. Que pensez-vous des commentaires laissés par le développeur principal ?

Le projet contient seulement **2 commentaires** :

```python
# Si get, afficher la page vide
# Si post, calculer et afficher le résultat
```

Ces commentaires sont **insuffisants et peu utiles** pour les raisons suivantes :

- **Ils n'apportent aucune information nouvelle** : ils répètent ce que le code dit déjà explicitement (`if request.method == 'GET':` est auto-explicatif).
- **Ils expliquent le "quoi" et non le "pourquoi"** : un bon commentaire devrait expliquer une décision non évidente (ex: pourquoi on utilise `int()` et pas `float()` pour les coordonnées).
- **Absence de commentaires là où ils seraient utiles** :
  - La formule de distance de Pythagore mériterait une explication
  - Les fonctions n'ont pas de **docstrings** décrivant les paramètres et valeurs de retour
  - Le code mort (`print` après `return`) n'est même pas signalé
- **Les variables peu claires** (`eNd`, `result_tmp`) n'ont aucune explication

En résumé, les commentaires présents sont redondants avec le code et les commentaires vraiment utiles sont absents.

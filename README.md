# 🚀 Projet réalisé avec Imene Belhocine

Ce repository contient un projet complet de traitement de données, d'initialisation de base de données, et d'API sécurisée avec FastAPI. Plusieurs scripts permettent également de tester la qualité des données et de manipuler les résultats.

---

## 🛠️ Lancement du projet

Avant tout, il est nécessaire de créer un environnement virtuel et d'installer les dépendances :

```bash
python -m venv .venv
source env/bin/activate  # Sur Windows : .venv\Scripts\activate
pip install -r requirements.txt
```

## Ordre de lancement des fichiers

Lancer les scripts dans l'ordre suivant :

    - generated_csv.py – Génère les fichiers CSV nécessaires.
    - init_db.py – Initialise la base de données avec les données générées.

## Démarrer le serveur

Une fois les étapes précédentes réalisées, vous pouvez lancer le serveur FastAPI : uvicorn backend.main:app --reload

## 🔐 Tester la sécurité

    Ouvrir le fichier test.http.
    Lancer la route POST /login pour récupérer un token JWT.
    Utiliser ce token pour appeler la route protégée GET /secure-data.

Un dossier logs sera automatiquement généré après les tests de sécurité, contenant tous les fichiers de log.

## Autres scripts

    duckdb_save.py : Permet de sauvegarder la base de données DuckDB.
    Dossier logs/ : Contient les journaux d’exécution après les tests de sécurité.

## Data Quality

Un test de qualité des données est disponible dans le notebook :

    Lancer le fichier image_processing.ipynb.
    Un dossier processed_images/ sera généré, contenant les images améliorées.

## Annexes

Vous trouverez notre modélisation Merise dans le dossier : database_models/

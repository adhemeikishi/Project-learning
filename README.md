# Projet IA: Classification d’Images

## But du projet

Développement d’un **modèle simple de classification d’images en Python**
Le projet permet de **mettre en pratique les bases de l’intelligence artificielle** : prétraitement des données, entraînement de modèle, évaluation et export des résultats.

---

## Compétences travaillées

* **Python** : structuration du projet, scripts modulaires
* **NumPy & Pandas** : manipulation de tableaux et DataFrames
* **Scikit-Learn** : pipeline de Machine Learning et classification d’images
* **Prétraitement de données** : resize, normalisation
* **Machine Learning** : entraînement, évaluation, prédiction
* **Automatisation de scripts** : création de pipelines de traitement et de test
* **Interface utilisateur** : Streamlit pour uploader et annoter les images

---

## Structure du projet

* `data/raw/` : images brutes organisées par classe
* `data/processed/` : sorties prétraitées (fichiers `.npz`)
* `src/` : scripts Python principaux

  * `data_prep.py` : prétraitement
  * `train.py` : entraînement du modèle
  * `evaluate.py` : évaluation et rapport
  * `predict.py` : prédiction sur nouvelles images
  * `utils.py` : fonctions utilitaires
* `models/` : modèles sauvegardés (`.joblib`)
* `outputs/` : graphiques, rapports et CSV
* `app/` : interface **Streamlit** pour labelling et test rapide

---

## Installation et préparation

1. Cloner le projet :

```bash
git clone <url-du-projet>
cd <nom-du-projet>
```

2. Créer un environnement virtuel :

```bash
python -m venv .venv
```

3. Activer l’environnement virtuel :

* Windows :

```bash
.venv\Scripts\activate
```

* macOS / Linux :

```bash
source .venv/bin/activate
```

4. Installer les dépendances :

```bash
pip install -r requirements.txt
```

5. Préparer vos données :

* Organiser vos images sous `data/raw/<classe>/*.jpg`

---

## Lancer l’interface Streamlit

```bash
streamlit run app/streamlit_labeler.py --server.port 8501
```

* Ouvrir dans le navigateur : `http://localhost:8501`
* Fonctionnalités :

  * Upload multiple d’images (jpg, jpeg, png)
  * Visualisation en grille de 3 colonnes
  * Assignation de catégories par image
  * Résumé des annotations dans un tableau interactif
  * Export CSV (téléchargement ou sauvegarde côté serveur)

---

## Exemples d’utilisation des scripts

1. Préparer les données :

```bash
python src/data_prep.py --data_dir data/raw --out data/processed/dataset.npz --img_size 64
```

2. Entraîner le modèle :

```bash
python src/train.py --input data/processed/dataset.npz --model models/model.joblib --classifier logistic
```

3. Évaluer le modèle :

```bash
python src/evaluate.py --input data/processed/dataset.npz --model models/model.joblib
```

4. Prédire sur de nouvelles images :

```bash
python src/predict.py --model models/model.joblib --image path/to/image.jpg
```

---

## Test rapide avec images d’exemple

1. Générer des images factices :

```bash
python src/generate_examples.py
```

2. Créer un modèle factice si nécessaire :

```bash
python src/create_dummy_model.py
```

3. Lancer le test automatique :

```bash
python scripts/test_ui_predictions.py
```

* Les résultats sont sauvegardés dans `outputs/predictions_examples.csv`

---

# Dockerisation du projet

Cette section décrit comment lancer et utiliser le projet via Docker, sans installer Python ni dépendances localement.

## Prérequis

- **Docker Desktop installé et lancé**
  - macOS / Windows : [Docker Desktop](https://www.docker.com/products/docker-desktop)
  - Linux : Docker Engine + Docker Compose v2

**Vérification :**
```bash
docker --version
docker compose version
```

## Lancement rapide (1 commande)

À la racine du projet :
```bash
cp .env.example .env
docker compose up -d --build
```

Une fois le conteneur lancé, l'application est accessible à l'adresse :

**http://localhost:8502**

Le port est configurable via le fichier `.env`.

## Fonctionnement des ports

- **Dans le conteneur :** Streamlit écoute sur le port `8501`
- **Sur la machine hôte :** le port est exposé via Docker Compose

**Exemple :**
```
localhost:8502 → conteneur:8501
```

Si le port est déjà utilisé, modifier dans `.env` :
```env
STREAMLIT_SERVER_PORT=8503
```

Puis relancer :
```bash
docker compose up -d
```

## Persistance des données

Les données générées par l'application sont persistées sur la machine hôte grâce aux volumes Docker.

**Volumes utilisés :**
- `./outputs` → export des fichiers CSV
- `./data` → données et exemples
- `./models` → modèles entraînés

Les fichiers restent disponibles même après un `docker compose down`.

## Vérification de l'état (Healthcheck)

Le conteneur inclut un healthcheck Streamlit.

**Vérification :**
```bash
docker compose ps
```

**Statut attendu :**
```
Up (healthy)
```

## Logs

Pour consulter les logs de l'application :
```bash
docker compose logs -f
```

## Arrêter l'application
```bash
docker compose down
```

Relancer ensuite est possible à tout moment :
```bash
docker compose up -d
```

## Nettoyage complet (optionnel)

Pour supprimer les conteneurs et l'image Docker locale :
```bash
docker compose down --rmi local
```

Les dossiers montés (`outputs`, `data`, `models`) ne sont pas supprimés.

## Mode développement (hors Docker)

Il est également possible de lancer l'application sans Docker (mode développement), mais Docker est la méthode recommandée pour garantir la reproductibilité.

## Résumé

- ✔ Projet dockerisé
- ✔ Lançable en 1 commande
- ✔ Reproductible sur n'importe quel poste
- ✔ Données persistantes
- ✔ Logs et healthcheck disponibles
- ✔ Configuration via `.env`

## Bonnes pratiques

* Commencer avec des images **petites** (ex: 64x64) pour tester rapidement
* Vérifier l’équilibre des classes
* Tester différents classifieurs (`logistic`, `knn`, `rf`)

* Ne versionner que les données brutes (`data/raw`) ; `data/processed` et `models` ne doivent pas être versionnés

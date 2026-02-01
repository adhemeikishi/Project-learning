"""Crée un modèle dummy et le sauvegarde dans models/model.joblib
Le modèle est un pipeline qui accepte des vecteurs d'images aplatis et prédit des classes.
Usage: python src/create_dummy_model.py
"""
import numpy as np
from sklearn.dummy import DummyClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import joblib
import os

MODEL_PATH = 'models/model.joblib'

# Définit des classes correspondant aux images d'exemple
classes = np.array(['classA', 'classB', 'classC', 'classA2'], dtype=object)

# Génère dataset aléatoire pour "entraîner" un dummy classifier
n_samples = 200
# correspond à la taille d'image utilisée pour la prédiction dans l'app (64x64 RGB)
n_features = 64 * 64 * 3
# crée des features aléatoires adaptées
X = np.random.RandomState(42).rand(n_samples, n_features)
y = np.random.choice(len(classes), size=n_samples)

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('pca', PCA(n_components=0.95, svd_solver='full')),
    ('clf', DummyClassifier(strategy='stratified', random_state=42))
])

# Fit sur les features synthétiques
pipeline.fit(X, y)

os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
joblib.dump({'pipeline': pipeline, 'classes': classes}, MODEL_PATH)
print('Dummy model saved to', MODEL_PATH)

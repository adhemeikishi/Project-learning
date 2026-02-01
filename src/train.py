"""Entraînement: charge dataset .npz, entraîne un classifieur sklearn, sauvegarde le modèle.

Usage:
  python src/train.py --input data/processed/dataset.npz --model models/model.joblib --classifier logistic

Options de classifieurs: logistic, knn, rf
"""
import argparse
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

CLASSIFIERS = {
    'logistic': LogisticRegression(max_iter=200),
    'knn': KNeighborsClassifier(n_neighbors=5),
    'rf': RandomForestClassifier(n_estimators=100, random_state=42)
}


def train_model(X, y, classifier='logistic', test_size=0.2, random_state=42):
    clf = CLASSIFIERS.get(classifier)
    if clf is None:
        raise ValueError('Classifier inconnu')
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('pca', PCA(n_components=0.95)),
        ('clf', clf)
    ])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    return pipeline, acc


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='Fichier .npz de dataset')
    parser.add_argument('--model', required=True, help='Chemin pour sauvegarder le modèle (joblib)')
    parser.add_argument('--classifier', default='logistic', choices=CLASSIFIERS.keys())
    args = parser.parse_args()

    data = np.load(args.input, allow_pickle=True)
    X = data['X']
    y = data['y']
    classes = data.get('classes')

    pipeline, acc = train_model(X, y, classifier=args.classifier)
    os.makedirs(os.path.dirname(args.model), exist_ok=True)

    # Sauvegarde d'un bundle contenant le pipeline et les classes (pratique pour l'inférence)
    model_bundle = {
        'pipeline': pipeline,
        'classes': classes
    }
    joblib.dump(model_bundle, args.model)
    print(f"Modèle (bundle) sauvegardé dans {args.model}. Accuracy sur split de test: {acc:.4f}")

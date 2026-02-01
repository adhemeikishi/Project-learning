"""Évaluation: charge modèle et dataset puis affiche métriques (accuracy, classification report, confusion matrix) et sauvegarde la matrice.

Usage:
  python src/evaluate.py --input data/processed/dataset.npz --model models/model.joblib --out outputs/confusion_matrix.png
"""
import argparse
import numpy as np
import joblib
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import os
import seaborn as sns

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--model', required=True)
    parser.add_argument('--out', default='outputs/confusion_matrix.png')
    args = parser.parse_args()

    data = np.load(args.input, allow_pickle=True)
    X = data['X']
    y = data['y']
    classes = data['classes']

    loaded = joblib.load(args.model)
    # prise en charge du bundle {'pipeline', 'classes'} ou d'un pipeline direct
    if isinstance(loaded, dict) and 'pipeline' in loaded:
        pipeline = loaded['pipeline']
        model_classes = loaded.get('classes', classes)
    else:
        pipeline = loaded
        model_classes = getattr(pipeline, 'classes_', classes)

    y_pred = pipeline.predict(X)

    acc = accuracy_score(y, y_pred)
    print(f"Accuracy (ensemble dataset): {acc:.4f}\n")
    print(classification_report(y, y_pred, target_names=model_classes))

    cm = confusion_matrix(y, y_pred)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', xticklabels=classes, yticklabels=classes, cmap='Blues')
    plt.xlabel('Prédiction')
    plt.ylabel('Vérité')
    plt.title('Matrice de confusion')
    plt.tight_layout()
    plt.savefig(args.out)
    print(f'Matrice de confusion sauvegardée dans {args.out}')

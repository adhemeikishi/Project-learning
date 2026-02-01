"""Prédiction: charge le modèle et prédit la classe pour une image donnée.

Usage:
  python src/predict.py --model models/model.joblib --image path/to/image.jpg
"""
import argparse
import joblib
from src.utils import load_image
import numpy as np


def preprocess_image(path, img_size=(64,64)):
    arr = load_image(path, img_size=img_size)
    return arr.reshape(1, -1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', required=True)
    parser.add_argument('--image', required=True)
    parser.add_argument('--img_size', type=int, default=64)
    args = parser.parse_args()

    loaded = joblib.load(args.model)

    # rétrocompatibilité: le modèle peut être soit un pipeline soit un bundle {'pipeline', 'classes'}
    if isinstance(loaded, dict) and 'pipeline' in loaded:
        pipeline = loaded['pipeline']
        classes = loaded.get('classes')
    else:
        pipeline = loaded
        classes = getattr(pipeline, 'classes_', None)

    X = preprocess_image(args.image, img_size=(args.img_size, args.img_size))
    pred = pipeline.predict(X)
    if classes is not None:
        print(f"Prediction: {classes[pred[0]]}")
    else:
        print(f"Prediction (label encodé): {pred[0]}")

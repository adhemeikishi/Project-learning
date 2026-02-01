"""Script de prétraitement: charge les images, redimensionne, normalise et enregistre dataset en .npz

Usage:
    python src/data_prep.py --data_dir data/raw --out data/processed/dataset.npz --img_size 64
"""
import argparse
import numpy as np
from sklearn.preprocessing import LabelEncoder
from src.utils import load_image, iterate_image_files
import os


def build_dataset(data_dir, img_size=(64, 64), flatten=True):
    images = []
    labels = []
    for path, label in iterate_image_files(data_dir):
        img = load_image(path, img_size=img_size)
        images.append(img)
        labels.append(label)
    X = np.array(images)
    y = np.array(labels)
    if flatten:
        # flatten images to vectors (n_samples, n_features)
        n = X.shape[0]
        X = X.reshape(n, -1)
    le = LabelEncoder()
    y_enc = le.fit_transform(y)
    return X, y_enc, le


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', required=True, help='Chemin vers data/raw')
    parser.add_argument('--out', required=True, help='Fichier de sortie .npz')
    parser.add_argument('--img_size', type=int, default=64, help='Taille (carrée) d\'une image')
    args = parser.parse_args()

    X, y, le = build_dataset(args.data_dir, img_size=(args.img_size, args.img_size))
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    np.savez_compressed(args.out, X=X, y=y, classes=le.classes_)
    print(f"Sauvegardé {X.shape[0]} images dans {args.out}")

"""Utils: fonctions communes pour chargement et prétraitement d'images."""
from PIL import Image
import numpy as np
import os


def load_image(path, img_size=(64, 64)):
    """Charge une image, la convertit en RGB, la redimensionne et retourne un array normalisé [0,1]."""
    with Image.open(path) as img:
        img = img.convert('RGB')
        img = img.resize(img_size)
        arr = np.asarray(img, dtype=np.float32) / 255.0
        return arr


def iterate_image_files(root_dir):
    """Parcours récursif: retourne (file_path, class_name) en supposant structure root/class_name/*.jpg"""
    for class_name in os.listdir(root_dir):
        class_dir = os.path.join(root_dir, class_name)
        if not os.path.isdir(class_dir):
            continue
        for fname in os.listdir(class_dir):
            if fname.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                yield os.path.join(class_dir, fname), class_name

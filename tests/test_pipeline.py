"""Test minimal: crée un petit dataset synthétique et vérifie que train_model s'exécute."""
import numpy as np
from src.train import train_model


def test_train_on_synthetic():
    # 100 échantillons, 64x64x3 flatten -> 12288 features
    n_samples = 100
    img_size = 32
    n_features = img_size * img_size * 3
    X = np.random.rand(n_samples, n_features).astype('float32')
    # deux classes équilibrées
    y = np.array([0] * (n_samples // 2) + [1] * (n_samples // 2))
    pipeline, acc = train_model(X, y, classifier='logistic')
    assert pipeline is not None
    assert 0.0 <= acc <= 1.0


if __name__ == '__main__':
    test_train_on_synthetic()
    print('Test synthétique OK')

"""Test automatique: génère exemples, crée un dummy model si nécessaire, et prédit sur les exemples.
Usage: python scripts/test_ui_predictions.py
"""
import os
import glob
import pandas as pd
import joblib
import subprocess

# 1) generate examples if not present
if not os.path.exists('data/examples') or not glob.glob('data/examples/*'):
    print('Generating example images...')
    subprocess.check_call(['python', 'src/generate_examples.py'])

# 2) create dummy model if missing
if not os.path.exists('models/model.joblib'):
    print('Creating dummy model...')
    subprocess.check_call(['python', 'src/create_dummy_model.py'])

# 3) load model
loaded = joblib.load('models/model.joblib')
if isinstance(loaded, dict) and 'pipeline' in loaded:
    pipeline = loaded['pipeline']
    classes = loaded.get('classes')
else:
    pipeline = loaded
    classes = getattr(pipeline, 'classes_', None)

# 4) predict on example images
paths = sorted(glob.glob('data/examples/*'))
results = []
for p in paths:
    try:
        from PIL import Image
        img = Image.open(p).convert('RGB')
        arr = img.resize((64,64))
        import numpy as np
        X = (np.asarray(arr, dtype=np.float32) / 255.0).reshape(1, -1)
        pred = pipeline.predict(X)[0]
        try:
            lab = classes[int(pred)]
        except Exception:
            lab = pred
        results.append((os.path.basename(p), lab))
    except Exception as e:
        results.append((os.path.basename(p), f'ERROR: {e}'))

# 5) save and print
os.makedirs('outputs', exist_ok=True)
df = pd.DataFrame(results, columns=['image','prediction'])
out_csv = 'outputs/predictions_examples.csv'
df.to_csv(out_csv, index=False)
print('Predictions saved to', out_csv)
print(df)

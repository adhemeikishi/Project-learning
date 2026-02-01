"""Génère des images d'exemple dans data/examples/ pour tester l'UI.
Usage: python src/generate_examples.py
"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT_DIR = 'data/examples'
os.makedirs(OUT_DIR, exist_ok=True)

examples = [
    ('classA', (255, 0, 0)),
    ('classB', (0, 255, 0)),
    ('classC', (0, 0, 255)),
    ('classA2', (255, 255, 0))
]

for i, (name, color) in enumerate(examples, start=1):
    img = Image.new('RGB', (128, 128), color=color)
    d = ImageDraw.Draw(img)
    text = name
    # draw text in center (best-effort; no font dependency)
    d.text((10, 54), text, fill=(255,255,255))
    path = os.path.join(OUT_DIR, f'{i:02d}_{name}.png')
    img.save(path)
    print('Saved', path)

print('Example images generated in', OUT_DIR)

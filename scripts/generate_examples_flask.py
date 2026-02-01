"""Generate example images for the Flask demo (data/examples)
Usage: python scripts/generate_examples_flask.py
"""
from PIL import Image, ImageDraw
import os

OUT = 'data/examples'
os.makedirs(OUT, exist_ok=True)
examples = [
    ('classA', (255, 0, 0)),
    ('classB', (0, 200, 0)),
    ('classC', (0, 0, 200)),
    ('classA2', (200, 200, 0)),
]
for i, (name, c) in enumerate(examples, start=1):
    img = Image.new('RGB', (800, 800), color=c)
    d = ImageDraw.Draw(img)
    d.text((30, 380), name, fill=(255,255,255))
    path = os.path.join(OUT, f'{i:02d}_{name}.png')
    img.save(path)
    print('Saved', path)
print('Done')
import os
from datetime import datetime
from PIL import Image

BASE_DIR = 'static/book_assets/'

def overlay_images():
    background = Image.open(os.path.join(BASE_DIR, 'background/sky.jpg'))
    midground = Image.open(os.path.join(BASE_DIR, 'midground/mountain.png'))
    character1 = Image.open(os.path.join(BASE_DIR, 'characters/hero.png'))

    # Make sure the overlays have an alpha channel for transparency
    background = background.convert("RGBA")
    midground = midground.convert("RGBA")
    character1 = character1.convert("RGBA")

    background.paste(midground, (0, 0), midground)
    background.paste(character1, (0, 0), character1)

    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    full_path = os.path.join('static/storybooks', current_time)
    os.makedirs(full_path, exist_ok=True)
    print(f'Created directory {full_path}')

    background.save(os.path.join(full_path, 'page-1.jpg'), "PNG")

overlay_images()

import os
import random
import json
from datetime import datetime
from PIL import Image

BASE_DIR = 'static/book_assets/'

def get_layer_assets(type):
    return [f for f in os.listdir(os.path.join(BASE_DIR, type)) if f.endswith('.png') or f.endswith('.jpg')]

def choose_asset(asset_type, asset_name, character_name=None):
    definitions_path = os.path.join(BASE_DIR, asset_type, 'definitions.json')

    with open(definitions_path, 'r') as file:
        definitions = json.load(file)

    if asset_name == "any":
        asset_name = random.choice(list(definitions.keys()))

    if asset_type != "characters":
        if asset_name in definitions:
            return os.path.join(BASE_DIR, asset_type, definitions[asset_name])
    else:
        for category, filenames in definitions.items():
            if category == asset_name:
                if character_name:
                    for filename in filenames:
                        if character_name in filename:
                            return os.path.join(BASE_DIR, asset_type, asset_name, filename)
                else:
                    return os.path.join(BASE_DIR, asset_type, asset_name, random.choice(filenames))

    return None


def create_page_image(page_number, hero=None, sidekick=None, villain=None):
    page_definitions_path = os.path.join(BASE_DIR, "page_definitions")

    with open(os.path.join(page_definitions_path, f"page_{page_number}.json"), 'r') as file:
        page_definition = json.load(file)

    canvas_size = (1028, 1028)
    canvas = Image.new("RGBA", canvas_size, (255, 255, 255, 255))

    bg_asset_path = choose_asset("background", page_definition.get("background", 'any'))
    # print('bg_asset_path', bg_asset_path)
    if bg_asset_path:
        bg_image = Image.open(bg_asset_path).convert("RGBA")
        canvas.paste(bg_image, (0, 0), bg_image)

    mg_asset_path = choose_asset("midground", page_definition.get("midground", 'any'))
    # print('mg_asset_path', mg_asset_path)
    if mg_asset_path:
        mg_image = Image.open(mg_asset_path).convert("RGBA")
        canvas.paste(mg_image, (0, 0), mg_image)

    sorted_characters = sorted(page_definition.get("characters", []), key=lambda x: x['zIndex'])

    for char_def in sorted_characters:
        char_type = char_def["type"]
        char_asset_path = None
        if char_type == "hero" and hero:
            char_asset_path = choose_asset("characters", char_type, hero)
        elif char_type == "sidekick" and sidekick:
            char_asset_path = choose_asset("characters", char_type, sidekick)
        elif char_type == "villain" and villain:
            char_asset_path = choose_asset("characters", char_type, villain)

        char_pos = char_def["position"]
        # print('char_asset_path', char_asset_path)
        if char_asset_path:
            char_image = Image.open(char_asset_path).convert("RGBA")
            canvas.paste(char_image, (char_pos["x"], char_pos["y"]), char_image)

    full_path = os.path.join("static/storybooks", datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))  # Update this path as needed
    os.makedirs(full_path, exist_ok=True)
    print(f'Created directory {full_path}')
    canvas.save(os.path.join(full_path, f"page-{page_number}.jpg"), "PNG")

create_page_image(1, hero='hero', sidekick='sidekick', villain='villain')
create_page_image(2, hero='hero2', sidekick='sidekick2', villain='villain2')
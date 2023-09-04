import re
import os
import requests
import io
import base64
import re
from datetime import datetime
from PIL import Image, PngImagePlugin
from util import read_file_content, replace_text, send_openai_message

MAX_RETRIES = 3
SD_URL = "http://127.0.0.1:7860"
context = []

# Step 1 - Generate outline
async def generate_outline(data):
    global context
    context = []
    for attempt in range(MAX_RETRIES):
        try:
            print(f"Generating outline attempt {attempt + 1}/{MAX_RETRIES}")
            prompt = read_file_content('prompts/step_1_prompt.txt')
            template = read_file_content('prompts/step_1_template.txt')
            for key, value in data.items():
                template = replace_text(template, f"{{{key}}}", value)
            story_outline, context = await send_openai_message(prompt, template, 'generate_outline')

            title, setting, characters = extract_outline_data(story_outline)
            return story_outline, title, setting, characters
        except Exception as e:
            print(f"Error in generate_outline: {e}")
    return None  # After retries are exhausted

# Step 1.5 - Extract data from outline for frontend
def extract_outline_data(story_outline):
    # Split this into chunks since the plot points list may match against the character regex
    # The prompt calls for +++ but we should prepare for formatting errors
    processed_lines = story_outline.split('+')
    # Get rid of empty lines or lines that contain a leftover +
    processed_lines = [line.strip() for line in processed_lines if line.strip() and '+' not in line]

    # print(processed_lines)

    title_match = re.search(r"Title: (.+)", processed_lines[0])
    title = title_match.group(1) if title_match else None

    setting_match = re.search(r"Setting: (.+)", processed_lines[1])
    setting = setting_match.group(1) if setting_match else None

    # Match a hypenated or numbered list
    characters_matches = re.findall(r"[\-|\d+\.] ([^:-]+)[\-:] (.+)", processed_lines[2])
    characters = {match[0]: match[1] for match in characters_matches} if characters_matches else {}

    if not len(title):
        raise Exception('Failed to extract title')
    elif not len(setting):
        raise Exception('Failed to extract setting')
    elif not len(characters):
        raise Exception('Failed to extract characters')

    return title, setting, characters

# Step 2 - Generate story content
async def generate_story_content(story_outline):
    global context
    for attempt in range(MAX_RETRIES):
        try:
            print(f"Generating story content attempt {attempt + 1}/{MAX_RETRIES}")
            prompt = read_file_content('prompts/step_2_prompt.txt')
            template = read_file_content('prompts/step_2_template.txt')
            template = replace_text(template, "{story_outline}", story_outline)
            story_lines, context = await send_openai_message(prompt, template, 'generate_story_lines', context)
            # The prompt calls for +++ but we should prepare for formatting errors
            processed_lines = story_lines.split('+')
            # Get rid of empty lines or lines that contain a leftover +
            processed_lines = [line.strip() for line in processed_lines if line.strip() and '+' not in line]
            return processed_lines
        except Exception as e:
            print(f"Error in generate_story_content: {e}")
    return None

# Step 3 - Generate image descriptions
async def generate_image_descriptions(story_lines):
    global context
    for attempt in range(MAX_RETRIES):
        try:
            print(f"Generating image descriptions attempt {attempt + 1}/{MAX_RETRIES}")
            # Rejoin the story lines into a single string for the prompt
            story_lines = "\n+++\n".join(story_lines)
            prompt = read_file_content('prompts/step_3_prompt.txt')
            template = read_file_content('prompts/step_3_template.txt')
            template = replace_text(template, "{story_lines}", story_lines)
            image_descriptions, context = await send_openai_message(prompt, template, 'generate_image_descriptions', context)
            return image_descriptions
        except Exception as e:
            print(f"Error in generate_image_descriptions: {e}")
    return None

# Step 4 - Generate Stable Diffusion prompts
async def generate_sd_prompts(image_descriptions):
    global context
    for attempt in range(MAX_RETRIES):
        try:
            print(f"Generating Stable Diffusion prompts attempt {attempt + 1}/{MAX_RETRIES}")
            prompt = read_file_content('prompts/step_4_prompt.txt')
            template = read_file_content('prompts/step_4_template.txt')
            template = replace_text(template, "{image_descriptions}", image_descriptions)
            sd_prompts, context = await send_openai_message(prompt, template, 'generate_sd_prompts', context)

            processed_prompts = sd_prompts.split('\n')
            processed_prompts = [prompt.strip() for prompt in processed_prompts if prompt.strip()]
            return processed_prompts
        except Exception as e:
            print(f"Error in generate_sd_prompts: {e}")
    return None

# Step 5 - Generate images
async def generate_images(processed_prompts):
    for attempt in range(MAX_RETRIES):
        try:
          print(f"Generating images attempt {attempt + 1}/{MAX_RETRIES}")
          current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
          full_path = os.path.join('static/storybooks', current_time)
          os.makedirs(full_path, exist_ok=True)
          print(f'Created directory {full_path}')

          for index, prompt in enumerate(processed_prompts):
              payload = {
                  "prompt": prompt,
                  "steps": 20
              }

              response = requests.post(url=f'{SD_URL}/sdapi/v1/txt2img', json=payload)
              resp_data = response.json()
              print(f'Generating image {index + 1}/{len(processed_prompts)}')

              for i in resp_data['images']:
                  image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

                  png_payload = {
                      "image": "data:image/png;base64," + i
                  }
                  response2 = requests.post(url=f'{SD_URL}/sdapi/v1/png-info', json=png_payload)

                  pnginfo = PngImagePlugin.PngInfo()
                  pnginfo.add_text("parameters", response2.json().get("info"))
                  image_save_path = os.path.join(full_path, f'page-{index + 1}.png')
                  image.save(image_save_path, pnginfo=pnginfo)
                  print(f'Generated image {index + 1}/{len(processed_prompts)}')

          print(f'Image generation complete!')
          return
        except Exception as e:
            print(f"Error in generate_images: {e}")

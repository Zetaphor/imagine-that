import os
from dotenv import load_dotenv
import io
import base64
import aiohttp
import cv2
from PIL import Image
import asyncio

load_dotenv()

API_URL = os.environ.get("SD_API_URL")

async def generate_masks(input_dir, output_dir):
  """
  Use Stable Diffusion to generate segmentation masks from images

  Args:
      input_dir (str): Path to the images
      output_dir (str): Path to save the masks
  """

  for file in os.listdir(input_dir):
    if (os.path.isdir(os.path.join(input_dir, file))):
       continue
    img = cv2.imread(os.path.join(input_dir, file))
    retval, bytes = cv2.imencode('.png', img)
    encoded_image = base64.b64encode(bytes).decode('utf-8')

    payload = {
      "width": img.shape[1],
      "height": img.shape[0],
      "controlnet_resize_mode": "Just Resize",
      "controlnet_module": "seg_ofcoco",
      "controlnet_input_images": [encoded_image],
      "controlnet_processor_res": 1024,
      "controlnet_threshold_a": 64,
      "controlnet_threshold_b": 64
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url=f'{API_URL}/controlnet/detect', json=payload) as response:
            if response.status != 200:
                raise ValueError(f"Request failed with status {response.status}")
            r = await response.json()

    image = Image.open(io.BytesIO(base64.b64decode(r['images'][0])))
    image.save(os.path.join(output_dir, f"{os.path.splitext(file)[0]}_mask.png"))


# asyncio.run(generate_masks('../test_images/isolated_test', '../test_images/mask_test/output'))
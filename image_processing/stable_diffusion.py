import io
import cv2
import base64
import aiohttp
from PIL import Image
import asyncio

async def txt2img_segmentation(input_image_path, positive_prompt, negative_prompt="", input_is_mask=False):
    """
    Generates an image from text, optionally returns a segmentation mask.

    Args:
        input_image_path (str): Path to the image.
        positive_prompt (str): Positive prompt.
        negative_prompt (str, optional): Negative prompt. Defaults to "".
        input_is_mask (bool, optional): Whether to return a segmentation mask. Defaults to False.

    Returns:
        Image: The generated image.
        Image (optional): The generated segmentation mask.
    """

    API_URL = "http://127.0.0.1:7860"

    img = cv2.imread(input_image_path)
    retval, bytes = cv2.imencode('.png', img)
    encoded_image = base64.b64encode(bytes).decode('utf-8')

    payload = {
        "prompt": positive_prompt,
        "negative_prompt": negative_prompt,
        "batch_size": 1,
        "steps": 20,
        "cfg_scale": 7,
        "alwayson_scripts": {
            "controlnet": {
                "args": [
                    {
                        "module": "none" if input_is_mask else "seg_ofcoco",
                        "alias": True,
                        "model": "controlnet11Models_seg [ab613144]",
                        "image": encoded_image,
                        # "weight": 1.0,
                        # "resize_mode": 1,
                        # "lowvram": False,
                        "processor_res": 1024,
                        # "threshold_a": 64,
                        # "threshold_b": 64,
                        # "guidance_start": 0.0,
                        # "guidance_end": 1.0,
                        # "control_mode": 0,
                        # "pixel_perfect": False
                    }
                ]
            }
        }
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url=f'{API_URL}/sdapi/v1/txt2img', json=payload) as response:
            if response.status != 200:
                raise ValueError(f"Request failed with status {response.status}")
            r = await response.json()

    if input_is_mask:
        image = Image.open(io.BytesIO(base64.b64decode(r['images'][0])))
        return image
    else:
        image = Image.open(io.BytesIO(base64.b64decode(r['images'][0])))
        mask = Image.open(io.BytesIO(base64.b64decode(r['images'][1])))
        return image, mask


async def generate_image_from_mask(input_image_path, positive_prompt, negative_prompt=""):
    """
    Generates an image from a mask.

    Args:
        input_image_path (str): Path to the image.
        positive_prompt (str): Positive prompt.
        negative_prompt (str): Negative prompt.

    Returns:
        Image: The generated image.
    """
    return await txt2img_segmentation(input_image_path, positive_prompt, negative_prompt, True)

async def generate_image_and_mask(input_image_path, positive_prompt, negative_prompt=""):
    """
    Generates an image from a mask.

    Args:
        input_image_path (str): Path to the image.
        positive_prompt (str): Positive prompt.
        negative_prompt (str): Negative prompt.

    Returns:
        Image: The generated image.
    """
    return await txt2img_segmentation(input_image_path, positive_prompt, negative_prompt, False)

# positive = 'illustration of a grassy field, masterpiece, trending on deviantart, (disney style:1.2), clouds'
# negative = 'frame, people, humans, characters'

# image = asyncio.run(generate_image_from_mask('mountain-segmentation.png', positive, negative))
# image.save('image-from-mask.png')

# image, mask = generate_image_and_mask('mountain.jpg', positive, negative)
# image.save('image-and-mask-image.png')
# mask.save('image-and-mask-mask.png')


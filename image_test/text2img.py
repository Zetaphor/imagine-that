import io
import cv2
import base64
import aiohttp
from PIL import Image
import asyncio

async def generate_image_from_text(input_image_path, output_image_path, positive_prompt, negative_prompt=""):
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
                        "module": "seg_ofcoco",
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

    print('Images', len(r['images']))
    image = Image.open(io.BytesIO(base64.b64decode(r['images'][0])))
    image.save(output_image_path)

    if len(r['images']) == 2:
        image = Image.open(io.BytesIO(base64.b64decode(r['images'][1])))
        image.save('second_' + output_image_path)
    return output_image_path


positive = 'illustration of a grassy field, masterpiece, trending on deviantart, (disney style:1.2), clouds'
negative = 'frame, people, humans, characters'
result = asyncio.run(generate_image_from_text('mountain.jpg', 'controlnetoutput.png', positive, negative))
print(result)


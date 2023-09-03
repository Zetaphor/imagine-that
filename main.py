import json
from quart import Quart, websocket, render_template
import story_generation

app = Quart(__name__)


@app.route('/')
async def index():
    return await render_template('template.html')

@app.websocket('/ws')
async def ws():
    while True:
        message_json = await websocket.receive()
        data = json.loads(message_json)

        # Step 1 - Generate outline
        await websocket.send(json.dumps({"status": "generating", "output": "outline"}))
        story_outline, title, setting, characters = await story_generation.generate_outline(data)
        if not story_outline:
            await websocket.send(json.dumps({"status": "error", "output": f"Failed to generate outline after {story_generation.MAX_RETRIES} retries"}))
            return
        else:
          await websocket.send(json.dumps({"status": "outline", "output": {"title": title, "setting": setting, "characters": characters}}))

        # # Step 2 - Generate story content
        await websocket.send(json.dumps({"status": "generating", "output": "content"}))
        # story_lines = await story_generation.generate_story_content(story_outline)
        # if not story_lines:
        #     await websocket.send(json.dumps({"status": "error", "output": f"Failed to generate story content after {story_generation.MAX_RETRIES} retries"}))
        #     return
        # else:
        #   await websocket.send(json.dumps({"status": "story_lines", "output": story_lines}))

        print('Story generation complete')
        # await websocket.send(json.dumps({"status": "complete", "output": "complete"}))

        # # Step 3 - Generate image descriptions
        # await websocket.send(json.dumps({"status": "generating", "output": "images"}))
        # image_descriptions = await story_generation.generate_image_descriptions(story_lines)
        # if not image_descriptions:
        #     await websocket.send(json.dumps({"status": "error", "output": f"Failed to generate image descriptions after {story_generation.MAX_RETRIES} retries"}))
        #     return

        # # Step 4 - Generate Stable Diffusion prompts
        # await websocket.send(json.dumps({"status": "generating", "output": "Generating Stable Diffusion prompts..."}))
        # sd_prompts = await story_generation.generate_sd_prompts(image_descriptions)
        # if not sd_prompts:
        #     await websocket.send(json.dumps({"status": "error", "output": f"Failed to generate SD prompts after {story_generation.MAX_RETRIES} retries"}))
        #     return

        # await websocket.send(json.dumps({"status": "generating", "output": "images"}))
        # await generate_images(sd_prompts)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
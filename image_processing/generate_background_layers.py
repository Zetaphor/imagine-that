from image_processing.stable_diffusion import generate_image_from_mask
from image_processing.separate_segmentation_layers import separate_segmentation_layers

async def generate_background_layers(mask_path, output_dir, positive_prompt, negative_prompt="", prefix=""):
  """
  Uses Stable Diffusion to generate a background image from a segmentation mask.
  It then separates the layers and saves them to the output directory.

  Args:
      mask_path (str): Path to the mask.
      output_dir (str): Path to save the layers.
      positive_prompt (str): Positive prompt.
      negative_prompt (str, optional): Negative prompt. Defaults to "".
      prefix (str, optional): Prefix for the output file names. Defaults to "".
  """
  image = await generate_image_from_mask(mask_path, positive_prompt, negative_prompt)
  # image.save('/home/zetaphor/Code/imagine-that/image_processing/tmp/stable-diffusion-output.png')

  # TODO: This is a hack so we can get the demo ready
  image.save(f"{output_dir}/{prefix}.png")
  # separate_segmentation_layers('/home/zetaphor/Code/imagine-that/image_processing/tmp/stable-diffusion-output.png', mask_path, output_dir, prefix=prefix)

# positive = 'illustration of a grassy field, masterpiece, trending on deviantart, (disney style:1.2), clouds'
# negative = 'frame, people, humans, characters'
# asyncio.run(generate_background_layers('../test_images/mountain-segmentation.png', './tmp', positive, negative, "test"))
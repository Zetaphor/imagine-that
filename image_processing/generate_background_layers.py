from stable_diffusion import generate_image_from_mask
from separate_segmentation_layers import separate_segmentation_layers

def generate_background_layers(mask_path, output_dir, positive_prompt, negative_prompt=""):
  """
  Uses Stable Diffusion to generate a background image from a segmentation mask.
  It then separates the layers and saves them to the output directory.

  Args:
      mask_path (str): Path to the mask.
      output_dir (str): Path to save the layers.
      positive_prompt (str): Positive prompt.
      negative_prompt (str, optional): Negative prompt. Defaults to "".
  """
  image = generate_image_from_mask(mask_path, positive_prompt, negative_prompt)
  image.save('./tmp/stable-diffusion-output.png')
  separate_segmentation_layers('./tmp/stable-diffusion-output.png', mask_path, output_dir)

# positive = 'illustration of a grassy field, masterpiece, trending on deviantart, (disney style:1.2), clouds'
# negative = 'frame, people, humans, characters'
# generate_background_layers('../image_test/mountain-segmentation.png', './tmp/final_layers', positive, negative)
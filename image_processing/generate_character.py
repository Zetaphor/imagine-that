from image_processing.stable_diffusion import generate_image_from_mask
from image_processing.separate_segmentation_layers import separate_segmentation_layers

def generate_character(mask_path, output_dir, positive_prompt, negative_prompt=""):
  """
  Uses Stable Diffusion to generate a character image from a segmentation mask.
  It then separates the layers and saves them to the output directory.

  Args:
      mask_path (str): Path to the mask.
      output_dir (str): Path to save the layers.
      positive_prompt (str): Positive prompt.
      negative_prompt (str, optional): Negative prompt. Defaults to "".
  """

  image = generate_image_from_mask(mask_path, positive_prompt, negative_prompt)
  image.save('./tmp/stable-diffusion-output.png')
  separate_segmentation_layers('./tmp/stable-diffusion-output.png', mask_path, output_dir, True)

# positive = '2d animation disney style giant angry monster (masterpiece:1.2) (cell shading) (animation) (flat color illustration:1.1) (best quality:1.2) (clean lines)'
# negative = '((large breasts)) (cleavage:1.2) (nude) (bloom) (photo photography photograph)  (saturated) (bad hands) (disfigured) (grain) (deformed) (poorly drawn) (mutilated) (lowres) (deformed) (lowpoly) (CG) (3d) (blurry) (out-of-focus) (depth_of_field) (duplicate) (frame) (border) (watermark) (label) (signature) (text) (cropped) (artifacts)'
# generate_character('../test_images/mask_test/output/villain_mask.png', '../test_images/generated_characters', positive, negative)
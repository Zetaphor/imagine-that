import os
from identify_segmentations import get_segmentation_colors
from process_segmentation import process_and_extract

def separate_segmentation_layers(source_image, mask_image, output_dir, crop=False, threshold=2):
  """
  Separate the layers of a segmentation mask.

  Args:
      source_image (str): Path to the source image.
      mask_image (str): Path to the mask image.
      output_dir (str): Path to save the separated layers.
      threshold (int, optional): Threshold value for color sensitivity. Defaults to 2.
  """
  filename = os.path.splitext(os.path.basename(source_image))[0]
  colors = get_segmentation_colors(mask_image, threshold)
  for index, (color, count) in enumerate(colors):
    process_and_extract(source_image, mask_image, color, 1, f'{output_dir}/{filename}_{index + 1}.png', crop)
    print(f'{output_dir}/{filename}_{index + 1}.png')

# separate_segmentation_layers('../image_test/text2img_output.png', '../image_test/mountain-segmentation.png', './layers', 2)
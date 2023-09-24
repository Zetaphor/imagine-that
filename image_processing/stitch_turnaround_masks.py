import os
from PIL import Image

def stitch_turnaround_sheet(coords, masks_dir, output_path):
  result_image = None

  for filename in coords.keys():
      current_image = Image.open(os.path.join(masks_dir, filename + "_mask.png"))

      if result_image is None:
          result_image = current_image.copy()
      else:
          width, height = current_image.size
          result_width, result_height = result_image.size
          new_width = result_width + width
          new_height = max(result_height, height)
          new_result_image = Image.new("RGB", (new_width, new_height))
          new_result_image.paste(result_image, (0, 0))
          new_result_image.paste(current_image, (result_width, 0))
          result_image = new_result_image

  result_image.save(os.path.join(output_path))


coordinates_dict = {
    "front": 0,
    "front-side": 184,
    "back-side": 364,
    "walking": 532,
    "jump": 782
}

stitch_turnaround_sheet(coordinates_dict, "./tmp/turnaround/masks", "tmp/turnaround/stitched_mask.png")
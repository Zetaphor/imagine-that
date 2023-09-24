import os
import asyncio
from image_processing.split_turnaround_sheet import split_turnaround
from image_processing.generate_masks import generate_masks
from image_processing.process_segmentation import process_and_extract
from image_processing.stable_diffusion import generate_image_from_mask
from image_processing.separate_segmentation_layers import separate_segmentation_layers

async def process_turnaround_sheet(sheet_path, coords, output_path):
  # Reset the tmp dirs
  os.system(f"rm -rf ./image_processing/tmp/turnaround")
  os.makedirs('./image_processing/tmp/turnaround/masks')
  os.makedirs('./image_processing/tmp/turnaround/generated')
  os.makedirs('./image_processing/tmp/turnaround/separated')


  # split_turnaround(sheet_path, coords, "./image_processing/tmp/turnaround")

  await generate_masks('./image_processing/tmp/isolated_test', './image_processing/tmp/turnaround/masks')

  positive = '2d animation disney style character (masterpiece:1.2) (cell shading) (animation) (flat color illustration:1.1) (best quality:1.2) (clean lines)'
  negative = '((large breasts)) (cleavage:1.2) (nude) (bloom) (photo photography photograph)  (saturated) (bad hands) (disfigured) (grain) (deformed) (poorly drawn) (mutilated) (lowres) (deformed) (lowpoly) (CG) (3d) (blurry) (out-of-focus) (depth_of_field) (duplicate) (frame) (border) (watermark) (label) (signature) (text) (cropped) (artifacts)'

  # Iterate each mask file in the tmp dir
  for filename in os.listdir('./image_processing/tmp/turnaround/masks'):
    mask_path = './image_processing/tmp/turnaround/masks/' + filename
    image = await generate_image_from_mask(mask_path, positive, negative)
    image.save('./image_processing/tmp/turnaround/generated/' + filename)
    separate_segmentation_layers('./image_processing/tmp/turnaround/generated/' + filename, mask_path, output_path, True)



coords = {
          "front": 0,
          "front-side": 184,
          "back-side": 364,
          "walking": 532,
          "jump": 782
        }
asyncio.run(process_turnaround_sheet("./test_images/Allan-Turnaround.png", coords, "./image_processing/tmp/turnaround/separated"))
import numpy as np
from PIL import Image

def rgb_to_hex(rgb):
    """Convert an RGB tuple to a hexadecimal color code."""
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])

def get_segmentation_colors(image_path, threshold=2):
    """
    Get unique colors from a segmentation map.
    Only returns colors that are above the threshold percentage of the total pixels.
    The Oneformer Coco model sometimes draws a line separating layers, a low threshold filters that out.

    Args:
        image_path (str): Path to the image.
        threshold (int, optional): Threshold percentage. Defaults to 2.

    Returns:
        list: List of unique colors with hex value and pixel count percentages.
    """
    image = Image.open(image_path)
    data = np.array(image)
    reshaped_data = data.reshape(-1, data.shape[2])

    unique_colors, counts = np.unique([tuple(pixel) for pixel in reshaped_data], axis=0, return_counts=True)

    sorted_indices = np.argsort(counts)[::-1]
    sorted_colors = unique_colors[sorted_indices]
    sorted_counts = counts[sorted_indices]

    total_pixels = data.shape[0] * data.shape[1]
    percentages = (sorted_counts / total_pixels) * 100

    sorted_colors_hex = [rgb_to_hex(color) for color in sorted_colors]

    # Filter the colors based on the threshold percentage
    filtered_colors = [(color, percentage) for color, percentage in zip(sorted_colors_hex, percentages) if percentage >= threshold]

    return filtered_colors

# # unique_colors_with_counts = get_unique_colors('image_test/grassy-hills-segmentation.png')
# unique_colors_with_percentages = get_segmentation_colors('image_test/grassy-hills-segmentation.png')

# for color, count in unique_colors_with_percentages:
#     print(f'{color} ({count})')

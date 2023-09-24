from PIL import Image

def split_turnaround(image_path, coordinates_dict, output_folder):
    """
    Splits an image into multiple sub-images based on a dictionary of filenames and horizontal split coordinates.

    Args:
    - image_path (str): Path to the image to be split.
    - coordinates_dict (dict): Dictionary where the key is the filename and the value is the horizontal coordinate for the split (left boundary).
    - output_folder (str): Folder where the split images will be saved.

    Returns:
    - List of split image paths.
    """
    img = Image.open(image_path)
    width, height = img.size

    sorted_coordinates = sorted(coordinates_dict.items(), key=lambda x: x[1])

    split_images = []

    for i in range(len(sorted_coordinates)):
        filename = sorted_coordinates[i][0]
        left = sorted_coordinates[i][1]

        # If it's the last coordinate, the right boundary is the image's width.
        # Otherwise, it's the next coordinate.
        right = width if i == len(sorted_coordinates) - 1 else sorted_coordinates[i + 1][1]

        split_img = img.crop((left, 0, right, height))

        split_image_path = f"{output_folder}/{filename}.png"
        split_img.save(split_image_path)
        split_images.append(split_image_path)

    return split_images

# coordinates_dict = {
#     "front": 0,
#     "front-side": 184,
#     "back-side": 364,
#     "walking": 532,
#     "jump": 782
# }

# split_turnaround("../test_images/Allan-Turnaround.png", coordinates_dict, "../test_images/turnaround_test")

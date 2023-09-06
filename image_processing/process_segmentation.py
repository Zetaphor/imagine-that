from PIL import Image
import numpy as np
import cv2

def hex_to_rgb(hex_color: str) -> tuple:
    hex_color = hex_color.lstrip('#')
    return (int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16))

def extract_mask(image_path: str, target_color: tuple, threshold: int) -> Image:
    """
    Extracts a mask from an image. Requires a target color for the mask and a threshold value for color sensitivity.
    So far a threshold of 1 seems to work with the Oneformer Coco preprocessor.

    Args:
        image_path (str): Path to the image.
        target_color (tuple): Target color for the mask.
        threshold (int): Threshold value for color sensitivity.

    Returns:
        Image: The extracted mask.
    """
    img = Image.open(image_path)
    img = img.convert("RGBA")
    data = np.array(img)

    lower_bound = np.array(target_color[:3]) - threshold
    upper_bound = np.array(target_color[:3]) + threshold

    mask_within_threshold = np.all((data[:, :, :3] >= lower_bound) & (data[:, :, :3] <= upper_bound), axis=2)
    data[mask_within_threshold, :3] = 0
    data[~mask_within_threshold, :3] = 255
    data[:, :, 3] = 255

    return Image.fromarray(data)

def extract_image_using_mask(source_img: np.ndarray, mask_img: Image, output_path) -> np.ndarray:
    """
    Extracts an image based on a provided mask. The output image will be cropped with a transparent background.

    Args:
        source_img (numpy.ndarray): Source image array.
        mask_img (Image): Mask image object.
        output_path (str): Path to save the extracted image.

    Returns:
        numpy.ndarray: The extracted and cropped image.
    """
    def save_with_transparency(source_img, binary_mask, output_path):
        b, g, r = cv2.split(source_img)
        rgba = [b, g, r, binary_mask]
        dst = cv2.merge(rgba, 4)
        cv2.imwrite(output_path, dst)

    mask_data = np.array(mask_img.convert('L'))
    _, binary_mask = cv2.threshold(mask_data, 127, 255, cv2.THRESH_BINARY_INV)

    extracted_img = cv2.bitwise_and(source_img, source_img, mask=binary_mask)

    # Convert the image to grayscale and threshold it
    gray = cv2.cvtColor(extracted_img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # If contours are found, find the largest one and get its bounding box
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        extracted_img = extracted_img[y:y+h, x:x+w]

    save_with_transparency(extracted_img, binary_mask[y:y+h, x:x+w], output_path)

    return extracted_img

def process_and_extract(source_image_path: str, mask_image_path: str, target_color: str, threshold: int, output_path: str):
    """
    Extracts an image based on a provided mask. The output image will be cropped with a transparent background.

    Args:
        source_image_path (str): Path to the source image.
        mask_image_path (str): Path to the mask image.
        target_color (str): Target color for the mask.
        threshold (int): Threshold value for color sensitivity.
        output_path (str): Path to save the extracted image.
    """
    mask_img = extract_mask(mask_image_path, hex_to_rgb(target_color), threshold)
    source_img = cv2.imread(source_image_path, cv2.IMREAD_COLOR)
    extract_image_using_mask(source_img, mask_img, output_path)

process_and_extract("image_test/source image.png", "image_test/mask.png", "#96053D", 1, "process-segmentation-output.png")

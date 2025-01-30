import numpy as np
import tqdm
from PIL import Image


def color_isolate(data, color, threshold=100, darken_amount=0.5):
    """
    Darkens the areas that are not the specified color.
    :param data: the data to color isolate
    :param color: the color to isolate (rgb)
    :param threshold: the threshold to isolate the color
    :param darken_amount: the amount to darken the isolated color
    :return: the color isolated data
    """
    darken_amount = 1 - darken_amount
    for d in tqdm.tqdm(data, desc="Isolating color"):
        image = d["image"]
        # Convert image to a NumPy array
        img_array = np.array(image)

        # Calculate the distance to the target color
        color_diff = np.abs(img_array[..., :3] - color)
        color_distance = np.sqrt(np.sum(color_diff ** 2, axis=-1))

        # Apply threshold to isolate the color
        mask = color_distance < threshold
        img_array[~mask] = np.clip(img_array[~mask] * darken_amount, 0, 255)

        # Convert back to image
        d["image"] = Image.fromarray(img_array)

    return data

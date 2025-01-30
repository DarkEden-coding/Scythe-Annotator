from concurrent.futures import ThreadPoolExecutor

import tqdm
from PIL import ImageFilter


def blur(data, factor=3, copy=True):
    """
    Blurs the data.
    :param data: the data to blur
    :param factor: the factor to blur the data by
    :param copy: whether to keep the original data and add the blurred data to it
    :return: the blurred data
    """
    def blur_image(d):
        if not copy:
            d["image"] = d["image"].filter(ImageFilter.GaussianBlur(factor))
            return d
        else:
            augment_value = d.get("augment_value", None)
            augment_value = augment_value + "b" if augment_value is not None else "b"

            return {"image": d["image"].filter(ImageFilter.GaussianBlur(factor)),
                    "annotations": d["annotations"],
                    "label_name": d["label_name"],
                    "image_name": d["image_name"],
                    "augment_value": augment_value}

    # Using ThreadPoolExecutor to process the data in parallel
    with ThreadPoolExecutor() as executor:
        blurred_data = list(
            tqdm.tqdm(executor.map(blur_image, data), desc="Blurring images", total=len(data))
        )

    if copy:
        return data + blurred_data
    return data

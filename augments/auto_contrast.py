import tqdm
from PIL import ImageOps


def auto_contrast(data):
    """
    Makes auto contrast permutations of the data.
    :param data: the data to make auto contrast
    :return: the auto contrast data
    """
    for d in tqdm.tqdm(data, desc="Auto contrasting images"):
        d["image"] = ImageOps.autocontrast(d["image"])
    return data
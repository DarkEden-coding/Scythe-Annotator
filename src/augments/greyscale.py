import tqdm

def greyscale_append(data):
    """
    Makes greyscale permutations of the data.
    :param data: the data to make greyscale
    :return: the greyscale data added to the original data
    """
    greyscale_data = []
    for d in tqdm.tqdm(data, desc="Greyscaling images:"):
        augment_value = d.get("augment_value", None)
        augment_value = augment_value + "g" if augment_value is not None else "g"

        greyscale_data.append({"image": d["image"].convert("L"), "annotations": d["annotations"], "label_name": d["label_name"], "image_name": d["image_name"], "augment_value": augment_value})
    return data + greyscale_data

def greyscale(data):
    """
    Makes greyscale permutations of the data.
    :param data: the data to make greyscale
    :return: the greyscale data
    """
    for d in tqdm.tqdm(data, desc="Greyscaling images:"):
        d["image"] = d["image"].convert("L")
    return data
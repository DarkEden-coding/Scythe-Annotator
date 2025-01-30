from concurrent.futures import ThreadPoolExecutor

import tqdm


def rotate(data):
    """
    Makes rotated permutations of the data. The data is rotated by 90, 180, and 270 degrees.
    :param data: the data to rotate
    :return: the rotated data added to the original data
    """
    def rotate_image(d):
        image_size = d["image"].size

        augment_value = d.get("augment_value", None)
        augment_value = augment_value + "r" if augment_value is not None else "r"

        rotated_90_size = (image_size[1], image_size[0])
        rotated_270_size = (image_size[1], image_size[0])

        rotated_data = []
        rotated_data.append({"image": d["image"].rotate(90, expand=1).resize(rotated_90_size),
                             "annotations": [a.copy().rotate(-90) for a in d["annotations"]] if d["annotations"] is not None else None,
                             "label_name": d["label_name"],
                             "image_name": d["image_name"],
                             "augment_value": augment_value})
        rotated_data.append({"image": d["image"].rotate(180, expand=1).resize(image_size),
                             "annotations": [a.copy().rotate(-180) for a in d["annotations"]] if d["annotations"] is not None else None,
                             "label_name": d["label_name"],
                             "image_name": d["image_name"],
                             "augment_value": augment_value + "1"})
        rotated_data.append({"image": d["image"].rotate(270, expand=1).resize(rotated_270_size),
                             "annotations": [a.copy().rotate(-270) for a in d["annotations"]] if d["annotations"] is not None else None,
                             "label_name": d["label_name"],
                             "image_name": d["image_name"],
                             "augment_value": augment_value + "2"})
        return rotated_data

    # Using ThreadPoolExecutor to process the data in parallel
    with ThreadPoolExecutor() as executor:
        rotated_data = list(
            tqdm.tqdm(executor.map(rotate_image, data), desc="Rotating images", total=len(data))
        )

    # Flatten the list of rotated data and append to the original data
    rotated_data = [item for sublist in rotated_data for item in sublist]
    return data + rotated_data

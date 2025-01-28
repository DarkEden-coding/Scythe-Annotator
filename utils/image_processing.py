import imagehash
from PIL import Image
from tqdm import tqdm


def hash_thread(image_paths):
    return [{"image": path, "hash": imagehash.average_hash(Image.open(path))} for path in image_paths]


def compair_hashes(hash1, hash2):
    return hash1 - hash2


def group_similar_images(image_hashes_and_paths, distance_threshold=5):
    groups = []
    for data in tqdm(image_hashes_and_paths, desc="Grouping similar images"):
        found = False
        for group in groups:
            if compair_hashes(data["hash"], group[0]["hash"]) < distance_threshold:
                group.append(data)
                found = True
                break
        if not found:
            groups.append([data])
    return [[data["image"] for data in group] for group in groups]

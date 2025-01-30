import tqdm

def resize(data, size = (640, 640)):
    for d in tqdm.tqdm(data, desc="Resizing images"):
        d["image"] = d["image"].resize(size)
    return data
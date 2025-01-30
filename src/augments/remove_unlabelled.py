import tqdm


def remove_unlabelled(data):
    print(f"Removing unlabelled data from {len(data)} images")
    def is_labelled(d):
        return d["annotations"] is not None and len(d["annotations"]) > 0
    print(f"Removed {len(data) - len([d for d in data if is_labelled(d)])} unlabelled images")
    return [d for d in tqdm.tqdm(data) if is_labelled(d)]

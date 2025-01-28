image_formats = [
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".webp",
    ".heic", ".heif", ".svg", ".raw", ".psd", ".ai", ".eps", ".ico",
    ".jfif", ".avif", ".pdf"  # (PDF is often treated as an image format)
]


def image_to_label_path(image_path: str) -> str:
    """
    Convert an image path to a label path by replacing the file extension with .txt
    :param image_path: The path to the image file
    :return: The path to the label file
    """
    for image_format in image_formats:
        if image_path.endswith(image_format):
            return image_path.replace(image_format, ".txt")
    return image_path + ".txt"


import tqdm
from PIL import ImageFilter


def edge_enhancement(data):
    """
    Enhances the edges of the data.
    :param data: the data to enhance the edges
    :param edge_color: the color of the edge
    :return: the edge enhanced data
    """
    edge_color = (0, 0, 255)
    # detect edges and set the color
    for d in tqdm.tqdm(data, desc="Enhancing edges"):
        edges = d["image"].filter(ImageFilter.FIND_EDGES).convert("RGB")
        mask = edges.convert("L")

        for x in range(edges.width):
            for y in range(edges.height):
                r, g, b = edges.getpixel((x, y))
                if r > 30 and g > 30 and b > 30:
                    edges.putpixel((x, y), edge_color)
        # put the edges on the original image
        d["image"] = d["image"].convert("RGB")
        d["image"].paste(edges, (0, 0), mask)
    return data

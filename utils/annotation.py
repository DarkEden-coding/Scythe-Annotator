import math


def rotate_point_around_point(x, y, angle, center_x, center_y):
    # Convert angle to radians
    radians = math.radians(angle)

    # Apply rotation formula
    x_rot = (x - center_x) * math.cos(radians) - (y - center_y) * math.sin(radians) + center_x
    y_rot = (x - center_x) * math.sin(radians) + (y - center_y) * math.cos(radians) + center_y

    return x_rot, y_rot

class Annotation:
    def __init__(self, data_string, class_names):
        self.data_string = data_string
        self.object_class = None

        self.canvas = None
        self.canvas_rect = None
        self.canvas_text = None

        self.class_colors = None
        self.width = None
        self.height = None

        data = data_string.split(" ")
        try:
            self.center_x, self.center_y, self.width, self.height = [float(i) for i in data[1:]]
        except ValueError:
            print(f"\033[38;5;214mWarning: Annotation data could not be parsed: {data_string}\033[0m")
            raise ValueError(f"Annotation data could not be parsed: {data_string}")
        self.object_class = class_names[int(data[0])]
        self.object_index = int(data[0])
        self.all_class_names = class_names

    def get_corners(self):
        x1 = self.center_x - self.width / 2
        y1 = self.center_y - self.height / 2
        x2 = self.center_x + self.width / 2
        y2 = self.center_y + self.height / 2
        return x1, y1, x2, y2

    def draw(self, canvas, class_colors, image_width, image_height):
        x1, y1, x2, y2 = self.get_corners()
        x1 = int(x1 * image_width)
        y1 = int(y1 * image_height) + canvas.winfo_height() / 2
        x2 = int(x2 * image_width)
        y2 = int(y2 * image_height) + canvas.winfo_height() / 2

        x1, y1, x2, y2, = abs(x1), abs(y1), abs(x2), abs(y2)

        self.canvas_rect = canvas.create_rectangle(x1, y1, x2, y2, outline=class_colors[self.object_index], width=2)
        self.canvas_text = canvas.create_text(x1 + 5, y1 + 5, text=self.object_class, anchor="nw", fill=class_colors[self.object_index])

        self.canvas = canvas
        self.class_colors = class_colors

    def delete(self):
        self.canvas.delete(self.canvas_rect)
        self.canvas.delete(self.canvas_text)

    def update(self, image_width, image_height):
        self.delete()
        self.object_index = self.all_class_names.index(self.object_class)
        self.draw(self.canvas, self.class_colors, image_width, image_height)

    def __repr__(self):
        return f"Annotation(center_x={self.center_x}, center_y={self.center_y}, width={self.width}, height={self.height}, object_class={self.object_class})"

    def __str__(self):
        return f"Annotation: {self.object_class} at ({self.center_x}, {self.center_y}) with width {self.width} and height {self.height}"

    def to_dict(self):
        return {
            "center_x": self.center_x,
            "center_y": self.center_y,
            "width": self.width,
            "height": self.height,
            "object_class": self.object_class
        }

    @classmethod
    def from_dict(cls, data):
        annotation = cls("", [])
        annotation.center_x = data["center_x"]
        annotation.center_y = data["center_y"]
        annotation.width = data["width"]
        annotation.height = data["height"]
        annotation.object_class = data["object_class"]
        return annotation

    def to_yolo_format(self):
        return f"{self.object_index} {self.center_x} {self.center_y} {self.width} {self.height}"

    def rotate(self, angle):
        # rotate around center of image
        self.center_x, self.center_y = rotate_point_around_point(self.center_x, self.center_y, angle, 0.5, 0.5)
        self.width, self.height = rotate_point_around_point(self.width, self.height, angle, 0, 0)
        self.width = abs(self.width)
        self.height = abs(self.height)
        return self

    def copy(self):
        return Annotation(self.data_string, self.all_class_names)

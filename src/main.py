import json
import os

import customtkinter as ctk

from button_frame import ButtonFrame
from image_frame import ImageFrame


class YOLOViewerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("YOLO Dataset Viewer")
        self.geometry("800x600")

        self.load_geometry()

        self.data = []
        self.class_names = []
        self.class_colors = []
        self.current_image_index = -1

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="cols")

        self.image_frame = ImageFrame(self.main_frame, self)
        self.image_frame.grid(row=0, column=1, rowspan=1, columnspan=3, sticky="nsew", padx=(5, 10), pady=10)

        self.button_frame = ButtonFrame(self.main_frame, self)
        self.button_frame.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="nsew", padx=(10, 5), pady=10)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def get_center(self):
        x = self.winfo_x()
        y = self.winfo_y()
        width = self.winfo_width()
        height = self.winfo_height()
        center_x = x + width // 2
        center_y = y + height // 2
        return center_x, center_y

    def next_image(self):
        if self.current_image_index < len(self.data) - 1:
            self.current_image_index += 1
            try:
                annotations = self.button_frame.get_augmented_annotating(self.data[self.current_image_index], self.class_names)
                self.data[self.current_image_index]["annotations"] = annotations
            except IndexError:
                print("!!Please add classes for augmented annotation to work!!")
            self.image_frame.load_image(self.data[self.current_image_index]["image"], self.data[self.current_image_index]["annotations"])
        else:
            print("No more images to show")

    def previous_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.image_frame.load_image(self.data[self.current_image_index]["image"], self.data[self.current_image_index]["annotations"])
        else:
            print("No more images to show")

    def load_geometry(self):
        if os.path.exists("window_geometry.json"):
            with open("window_geometry.json", "r") as f:
                data = json.load(f)
                geometry = data.get("geometry", "800x600+100+100")
                self.geometry(geometry)

    def save_geometry(self):
        geometry = self.geometry()
        data = {"geometry": geometry}
        with open("window_geometry.json", "w") as f:
            json.dump(data, f)

    def on_closing(self):
        self.save_geometry()
        self.destroy()


if __name__ == "__main__":
    app = YOLOViewerApp()
    app.mainloop()

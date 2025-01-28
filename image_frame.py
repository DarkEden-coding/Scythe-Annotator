import random

import customtkinter as ctk
from PIL import ImageTk

from dialogs.annotation_edit_dialog import AnnotationEditDialog
from dialogs.class_edit_dialog import ClassEditDialog
from utils.annotation import Annotation


class ImageFrame(ctk.CTkFrame):
    def __init__(self, parent, parent_window):
        super().__init__(parent)
        self.parent_window = parent_window
        self.image = None

        self.current_bounding_box = None  # To store the current bounding box ID
        self.current_start_x = None  # Start x-coordinate for bounding box
        self.current_start_y = None  # Start y-coordinate for bounding box
        self.current_end_x = None  # End x-coordinate for bounding box
        self.current_end_y = None  # End y-coordinate for bounding box

        self.width = 0
        self.height = 0

        self.annotations = []

        self.grid_rowconfigure(0, weight=3)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.canvas = ctk.CTkCanvas(self)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.config(background="#333333", borderwidth=0, highlightthickness=0)

        # Bind motion events to the canvas
        self.canvas.bind("<ButtonPress-1>", self.mouse_down)
        self.canvas.bind("<B1-Motion>", self.mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_up)
        self.canvas.bind("<Motion>", self.guide_cursor)

        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=1, column=0, sticky="sew", padx=10, pady=10, ipady=5)

        self.button_frame.grid_rowconfigure(0, weight=1)
        self.button_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform="cols")

        self.class_var = ctk.StringVar(value="Select Class")
        self.class_menu = ctk.CTkOptionMenu(
            self.button_frame, values=["Select Class"], variable=self.class_var
        )
        self.class_menu.grid(row=0, column=0, rowspan=1, columnspan=2, sticky="ew", padx=10, pady=5)

        self.edit_classes_button = ctk.CTkButton(
            self.button_frame, text="Edit Classes", command=self.edit_classes
        )
        self.edit_classes_button.grid(row=0, column=2, rowspan=1, columnspan=1, sticky="ew", padx=10, pady=5)

        self.action_type_var = ctk.StringVar(value="Cursor")
        self.action_type_button = ctk.CTkSegmentedButton(
            self.button_frame, values=["Cursor", "Bounding Box"], variable=self.action_type_var
        )
        self.action_type_button.grid(row=0, column=3, rowspan=1, columnspan=1, sticky="ew", padx=10, pady=5)

    def load_image(self, image, annotations):
        self.canvas.delete("all")
        self.annotations = annotations
        if self.annotations is None:
            self.annotations = []
        self.image = image

        self.width, self.height = self.image.size
        if self.width > self.height:
            new_width = 600
            new_height = int(self.height * (new_width / self.width))
        else:
            new_height = 600
            new_width = int(self.width * (new_height / self.height))
        self.image = self.image.resize((new_width, new_height))
        self.width, self.height = new_width, new_height

        self.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, self.canvas.winfo_height() / 2, image=self.image, anchor="nw")

        if self.annotations:
            for annotation in self.annotations:
                annotation.draw(self.canvas, self.parent_window.class_colors, new_width, new_height)

        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def guide_cursor(self, event):
        self.canvas.delete("crosshair")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        self.canvas.create_line(0, event.y, canvas_width, event.y, fill="teal", dash=(2, 2), tags="crosshair", width=2)
        self.canvas.create_line(event.x, 0, event.x, canvas_height, fill="teal", dash=(2, 2), tags="crosshair", width=2)

    def mouse_down(self, event):
        if self.action_type_var.get() == "Cursor":
            self.click_edit_query(event)
        else:
            self.start_box(event)

    def mouse_up(self, event):
        if self.action_type_var.get() == "Cursor":
            pass
        else:
            self.finish_box(event)

    def mouse_drag(self, event):
        if self.action_type_var.get() == "Cursor":
            self.guide_cursor(event)
        else:
            self.update_box(event)
            self.guide_cursor(event)

    def click_edit_query(self, event):
        x, y = event.x, event.y
        for annotation in self.annotations:
            x1, y1, x2, y2 = annotation.get_corners()
            x1 = int(x1 * self.width)
            y1 = int(y1 * self.height)
            x2 = int(x2 * self.width)
            y2 = int(y2 * self.height)

            y1 += self.canvas.winfo_height() / 2
            y2 += self.canvas.winfo_height() / 2

            if x1 <= x <= x2 and y1 <= y <= y2:
                dialog = AnnotationEditDialog(self, self.parent_window, annotation, start_location=self.parent_window.get_center())
                self.wait_window(dialog)
                if dialog.annotation_deleted:
                    self.annotations.remove(annotation)
                    self.parent_window.data[self.parent_window.current_image_index]["annotations"] = self.annotations
                else:
                    annotation.update(self.width, self.height)
                    self.parent_window.data[self.parent_window.current_image_index]["annotations"] = self.annotations
                break

    def start_box(self, event):
        # Save the starting point
        self.current_start_x, self.current_start_y = event.x, event.y
        self.current_end_x, self.current_end_y = event.x, event.y
        # Create the bounding box (a rectangle)
        self.current_bounding_box = self.canvas.create_rectangle(
            self.current_start_x, self.current_start_y, self.current_start_x, self.current_start_y, outline="blue", width=3
        )

    def update_box(self, event):
        if self.current_bounding_box:
            # Update the rectangle's dimensions as the mouse moves
            self.canvas.coords(self.current_bounding_box, self.current_start_x, self.current_start_y, event.x, event.y)
            self.current_end_x, self.current_end_y = event.x, event.y

    def finish_box(self, event):
        if self.current_bounding_box:
            x1, y1, x2, y2 = self.current_start_x, self.current_start_y, self.current_end_x, self.current_end_y

            # reject boxes that are too small
            if abs(x2 - x1) < 10 or abs(y2 - y1) < 10:
                self.canvas.delete(self.current_bounding_box)
                self.current_bounding_box = None
                self.current_start_x, self.current_start_y = None, None
                return

            y1 -= self.canvas.winfo_height() / 2
            y2 -= self.canvas.winfo_height() / 2

            x1 /= self.width
            x2 /= self.width
            y1 /= self.height
            y2 /= self.height

            # Create the annotation
            annotation = Annotation(f"{self.parent_window.class_names.index(self.class_var.get()) if self.class_var.get() is not None else None} {((x1 + x2) / 2)} {((y1 + y2) / 2)} {x2 - x1} {y2 - y1}", self.parent_window.class_names)
            self.annotations.append(annotation)
            annotation.draw(self.canvas, self.parent_window.class_colors, self.width, self.height)

            self.parent_window.data[self.parent_window.current_image_index]["annotations"] = self.annotations

            self.canvas.delete(self.current_bounding_box)
            self.current_bounding_box = None
            self.current_start_x, self.current_start_y = None, None

    def edit_classes(self):
        class_edit_dialog = ClassEditDialog(self, self.parent_window.class_names, start_location=self.parent_window.get_center())
        self.wait_window(class_edit_dialog)
        new_classes = class_edit_dialog.classes

        if new_classes:
            self.parent_window.class_names = new_classes
            self.class_var.set("Select Class")
            self.class_menu.configure(values=self.parent_window.class_names)
            self.parent_window.class_colors = [
                "#%06x" % random.randint(0, 0xFFFFFF) for _ in range(len(self.parent_window.class_names))
            ]

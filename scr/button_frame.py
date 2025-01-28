import os
import pickle

import customtkinter as ctk
from PIL import Image

from dialogs.loading_dialog import LoadingDialog
from utils.annotation import Annotation
from utils.augmented_annotating import AugmentedAnnotating
from utils.export_data import export_dataset
from utils.load_data import load_yolo_dataset, load_raw_data

current_path = os.path.dirname(os.path.abspath(__file__))


class ButtonFrame(ctk.CTkFrame):
    def __init__(self, parent, parent_window):
        super().__init__(parent)
        self.parent_window = parent_window
        self.augmented_annotating_boolean = False
        self.augmented_annotating = None

        self.grid_rowconfigure([i for i in range(0, 10)], weight=1, uniform="rows")
        self.grid_columnconfigure((0, 1), weight=1, uniform="cols")

        self.load_dataset_button = ctk.CTkButton(self, text="Load Dataset", command=self.load_yolo_dataset)
        self.load_dataset_button.grid(row=0, column=0, rowspan=1, columnspan=2, sticky="nsew", padx=10, pady=(10, 5))

        self.load_raw_data_button = ctk.CTkButton(self, text="Load Raw Data", command=self.load_raw_data)
        self.load_raw_data_button.grid(row=1, column=0, rowspan=1, columnspan=2, sticky="nsew", padx=10, pady=(5, 5))

        self.next_button = ctk.CTkButton(self, text="Next", command=self.parent_window.next_image)
        self.next_button.grid(row=2, column=1, rowspan=1, columnspan=1, sticky="nsew", padx=(5, 10), pady=5)
        self.next_button.configure(state="disabled")

        self.previous_button = ctk.CTkButton(self, text="Previous", command=self.parent_window.previous_image)
        self.previous_button.grid(row=2, column=0, rowspan=1, columnspan=1, sticky="nsew", padx=(10, 5), pady=5)
        self.previous_button.configure(state="disabled")

        self.export_button = ctk.CTkButton(self, text="Export Dataset", command=self.export_dataset)
        self.export_button.grid(row=3, column=0, rowspan=1, columnspan=2, sticky="nsew", padx=10, pady=5)

        self.save_button = ctk.CTkButton(self, text="Save", command=self.save_state)
        self.save_button.grid(row=6, column=0, rowspan=1, columnspan=1, sticky="nsew", padx=10, pady=5)

        self.load_button = ctk.CTkButton(self, text="Load", command=self.load_state)
        self.load_button.grid(row=6, column=1, rowspan=1, columnspan=1, sticky="nsew", padx=10, pady=5)

        self.augmented_annotating_confidence_label = ctk.CTkLabel(self, text="Min Confidence:")
        self.augmented_annotating_confidence_label.grid(row=8, column=0, rowspan=1, columnspan=1, sticky="nsew", padx=10, pady=5)

        self.augmented_annotating_confidence_entry = ctk.CTkEntry(self, placeholder_text="0.5")
        self.augmented_annotating_confidence_entry.grid(row=8, column=1, rowspan=1, columnspan=1, sticky="nsew", padx=10, pady=5)
        self.augmented_annotating_confidence_entry.configure(state="disabled")

        self.load_augmented_ai_model_button = ctk.CTkButton(self, text="Load Augmented AI Model", command=self.load_augmented_ai_model)
        self.load_augmented_ai_model_button.grid(row=9, column=0, rowspan=1, columnspan=2, sticky="nsew", padx=10, pady=5)

        self.switch_var = ctk.BooleanVar(value=False)
        self.enable_augmented_annotating_switch = ctk.CTkSwitch(self, text="Enable Augmented Annotating", command=self.enable_augmented_annotating, variable=self.switch_var, onvalue=True, offvalue=False)
        self.enable_augmented_annotating_switch.grid(row=10, column=0, rowspan=1, columnspan=2, sticky="nsew", padx=10, pady=5)
        self.enable_augmented_annotating_switch.configure(state="disabled")

    def save_state(self):
        for i, data in enumerate(self.parent_window.data):

            if os.path.exists(os.path.join("save", f"data_{i}")):
                for file in os.listdir(os.path.join("save", f"data_{i}")):
                    os.remove(os.path.join("save", f"data_{i}", file))
                os.rmdir(os.path.join("save", f"data_{i}"))

            os.mkdir(os.path.join("save", f"data_{i}"))

            data["image"].save(os.path.join("save", f"data_{i}", data["image_name"]))

            if data["annotations"]:
                for j, annotation in enumerate(data["annotations"]):
                    with open(os.path.join("save", f"data_{i}", f"annotation_{j}.txt"), "w") as f:
                        f.write(annotation.to_yolo_format())

            # save the image name, label name, and class names with pickle
            pickle.dump((data["image_name"], data["label_name"], self.parent_window.class_names, self.parent_window.class_colors), open(os.path.join("save", f"data_{i}", "data.txt"), "wb"))

    def load_state(self):
        self.parent_window.data = []
        for i in range(len(os.listdir("save"))):
            data = {}
            data["image_name"], data["label_name"], class_names, class_colors = pickle.load(open(os.path.join("save", f"data_{i}", "data.txt"), "rb"))
            self.parent_window.class_colors = class_colors
            self.parent_window.class_names = class_names

            data["image"] = Image.open(os.path.join("save", f"data_{i}", data["image_name"]))

            annotations = []
            for j in range(len(os.listdir(os.path.join("save", f"data_{i}"))) - 2):
                with open(os.path.join("save", f"data_{i}", f"annotation_{j}.txt"), "r") as f:
                    line = f.read()
                    annotations.append(Annotation(line, class_names))

            data["annotations"] = annotations
            self.parent_window.data.append(data)

        self.parent_window.current_image_index = -1
        self.parent_window.next_image()
        self.next_button.configure(state="normal")
        self.previous_button.configure(state="normal")

    def load_yolo_dataset(self):
        load_yolo_dataset(self)

    def load_raw_data(self):
        load_raw_data(self)

    def export_dataset(self):
        export_dataset(self.parent_window, ctk)

    def enable_augmented_annotating(self):
        self.augmented_annotating_boolean = self.switch_var.get()
        if self.augmented_annotating_boolean:
            self.enable_augmented_annotating_switch.configure(text="Disable Augmented Annotating")
        else:
            self.enable_augmented_annotating_switch.configure(text="Enable Augmented Annotating")

    def load_augmented_ai_model(self):
        model_path = ctk.filedialog.askopenfilename(initialdir=current_path, title="Select a model", filetypes=(("Model files", "*.pt"),))
        if model_path:
            dialog = LoadingDialog("Loading model", self.parent_window.get_center())
            self.augmented_annotating = AugmentedAnnotating(model_path)
            self.enable_augmented_annotating_switch.configure(state="normal")
            self.augmented_annotating_confidence_entry.configure(state="normal")
            print("Model loaded")
            dialog.close()
        else:
            print("No model selected")

    def get_augmented_annotating(self, data, class_names):
        if not data["annotations"] and self.augmented_annotating_boolean:
            image = data["image"]
            return self.augmented_annotating.detect_objects(image, class_names, float(self.augmented_annotating_confidence_entry.get()) if self.augmented_annotating_confidence_entry.get() else 0.5)
        else:
            return data["annotations"]

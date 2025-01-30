import customtkinter as ctk


class AnnotationEditDialog(ctk.CTkToplevel):
    def __init__(self, parent, parent_window, current_annotation, start_location=None):
        super().__init__(parent)
        self.title("Edit Annotation")
        self.geometry(f"400x100+{start_location[0] - 200}+{start_location[1] - 50}" if start_location else "400x100")
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1, uniform="cols")
        self.grid_columnconfigure(1, weight=1, uniform="cols")
        self.parent_window = parent_window
        self.parent = parent

        self.annotation_deleted = False

        self.delete_button = ctk.CTkButton(self, text="Delete", command=self.delete_annotation)
        self.delete_button.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.class_selection_var = ctk.StringVar(value=current_annotation.object_class)
        self.class_selection = ctk.CTkOptionMenu(self, values=self.parent_window.class_names, variable=self.class_selection_var)
        self.class_selection.grid(row=0, column=0, sticky="ew", padx=10, pady=10, columnspan=2)

        self.save_button = ctk.CTkButton(self, text="Save", command=self.save_annotation)
        self.save_button.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        self.current_annotation = current_annotation

        self.grab_set()

    def delete_annotation(self):
        self.current_annotation.delete()
        self.annotation_deleted = True
        self.destroy()

    def save_annotation(self):
        self.current_annotation.object_class = self.class_selection_var.get()
        self.destroy()



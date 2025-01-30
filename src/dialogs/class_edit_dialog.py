import tkinter as tk

import customtkinter as ctk


class ClassEditDialog(ctk.CTkToplevel):
    def __init__(self, parent, classes=None, start_location=None):
        super().__init__(parent)

        if classes is None:
            self.classes = []
        else:
            self.classes = classes

        self.entry = None
        self.listbox = None

        self.geometry(f"400x400+{start_location[0] - 200}+{start_location[1] - 50}" if start_location else "400x400")
        self.title("Class Selector")
        self.create_widgets()

        self.grab_set()

    def create_widgets(self):
        # Entry for new strings
        entry_frame = ctk.CTkFrame(self)
        entry_frame.pack(pady=10, padx=10, fill="x")

        entry_label = ctk.CTkLabel(entry_frame, text="Enter a string:")
        entry_label.pack(side="left", padx=(10, 5))

        self.entry = ctk.CTkEntry(entry_frame, placeholder_text="New string")
        self.entry.pack(side="left", expand=True, fill="x", padx=(0, 5))

        add_button = ctk.CTkButton(entry_frame, text="Add", command=self.add_string)
        add_button.pack(side="left", padx=(5, 10))

        # Listbox to display strings
        listbox_frame = ctk.CTkFrame(self)
        listbox_frame.pack(pady=(10, 5), padx=10, expand=True, fill="both")

        listbox_label = ctk.CTkLabel(listbox_frame, text="String List:")
        listbox_label.pack(anchor="w", padx=10, pady=(5, 0))

        self.listbox = tk.Listbox(listbox_frame, height=15)
        self.listbox.pack(expand=True, fill="both", padx=10, pady=5)

        for class_name in self.classes:
            self.listbox.insert(ctk.END, class_name)
            self.entry.delete(0, ctk.END)

        # Remove button
        remove_button = ctk.CTkButton(self, text="Remove Selected", command=self.remove_selected)
        remove_button.pack(pady=(5, 10))

    def add_string(self):
        new_string = self.entry.get()
        if new_string:
            self.listbox.insert(ctk.END, new_string)
            self.entry.delete(0, ctk.END)
            self.classes.append(new_string)

    def remove_selected(self):
        selected_items = self.listbox.curselection()
        for index in reversed(selected_items):
            self.listbox.delete(index)
            self.classes.pop(index)

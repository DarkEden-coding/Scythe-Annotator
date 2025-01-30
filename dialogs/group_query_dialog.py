from tkinter import ttk

import customtkinter as ctk
from PIL import Image, ImageTk


class GroupQueryDialog(ctk.CTkToplevel):
    def __init__(self, parent, removed_groups, parent_window, start_location=None):
        super().__init__(parent)
        self.title("Confirm Exclusion of Similar Images")
        self.geometry(f"800x600 + {start_location[0] - 400} + {start_location[1] - 300}" if start_location else "800x600")
        self.removed_groups = removed_groups
        self.selected_to_remove = []
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        bg_color = parent_window._apply_appearance_mode(ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
        text_color = parent_window._apply_appearance_mode(ctk.ThemeManager.theme["CTkLabel"]["text_color"])
        selected_color = parent_window._apply_appearance_mode(ctk.ThemeManager.theme["CTkButton"]["fg_color"])

        treestyle = ttk.Style()
        treestyle.theme_use('default')
        treestyle.configure("Treeview", background=bg_color, foreground=text_color, fieldbackground=bg_color,
                            borderwidth=0)
        treestyle.map('Treeview', background=[('selected', bg_color)], foreground=[('selected', selected_color)])

        self.tree = ttk.Treeview(self, columns=("Group", "Image"), show="tree")
        self.tree.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        self.tree.bind("<ButtonRelease-1>", self.on_item_click)

        self.image_preview_label = ctk.CTkLabel(self, text="Image Preview", width=300, height=300, anchor="center")
        self.image_preview_label.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

        self.confirm_button = ctk.CTkButton(self, text="Confirm Exclusion", command=self.confirm_removal)
        self.confirm_button.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        self.cancel_button = ctk.CTkButton(self, text="Cancel", command=self.cancel_removal)
        self.cancel_button.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)

        self.populate_tree()
        self.result = None
        self.grab_set()

    def populate_tree(self):
        for idx, group in enumerate(self.removed_groups):
            parent = self.tree.insert("", "end", text=f"Group {idx + 1}")
            for image_path in group:
                self.tree.insert(parent, "end", text=image_path, values=(image_path,))

    def on_item_click(self, event):
        selected_item = self.tree.focus()
        image_path = self.tree.item(selected_item, "values")
        if image_path:
            self.show_image_preview(image_path[0])

    def show_image_preview(self, image_path):
        try:
            image = Image.open(image_path)
            image.thumbnail((300, 300))
            photo = ImageTk.PhotoImage(image)
            self.image_preview_label.configure(image=photo)
            self.image_preview_label.image = photo
        except Exception as e:
            self.image_preview_label.configure(text=f"Error loading image: {e}")
            self.image_preview_label.image = None

    def confirm_removal(self):
        self.result = True
        self.destroy()

    def cancel_removal(self):
        self.result = False
        self.destroy()

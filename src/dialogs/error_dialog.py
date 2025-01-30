import customtkinter as ctk


class ErrorDialog(ctk.CTkToplevel):
    def __init__(self, parent, parent_window, message, start_location=None):
        super().__init__(parent)
        self.title("!! Error !!")
        self.geometry(f"400x100+{start_location[0] - 200}+{start_location[1] - 50}" if start_location else "400x100")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1, uniform="cols")
        self.parent_window = parent_window
        self.parent = parent

        self.label = ctk.CTkLabel(self, text=message)
        self.label.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

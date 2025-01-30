import customtkinter as ctk

from dialogs.error_dialog import ErrorDialog


class ImageSeparationDialog(ctk.CTkToplevel):
    def __init__(self, parent, parent_window, start_location=None):
        super().__init__(parent)
        self.title("Select Image Separation Percentages")
        self.geometry(f"400x200+{start_location[0] - 200}+{start_location[1] - 50}" if start_location else "400x200")
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1, uniform="cols")
        self.grid_columnconfigure(1, weight=1, uniform="cols")
        self.grid_columnconfigure(2, weight=1, uniform="cols")
        self.parent_window = parent_window
        self.parent = parent

        self.train_percentage = 70
        self.test_percentage = 20
        self.validate_percentage = 10

        self.label = ctk.CTkLabel(self, text="Enter the percentages of train, test, and validate to separate:")
        self.label.grid(row=0, column=0, sticky="ew", padx=10, pady=10, columnspan=3)

        self.train_entry = ctk.CTkEntry(self)
        self.train_entry.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.train_entry.insert(0, str(self.train_percentage))
        self.train_entry.focus_force()

        self.test_entry = ctk.CTkEntry(self)
        self.test_entry.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        self.test_entry.insert(0, str(self.test_percentage))

        self.validate_entry = ctk.CTkEntry(self)
        self.validate_entry.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)
        self.validate_entry.insert(0, str(self.validate_percentage))

        self.save_button = ctk.CTkButton(self, text="Save", command=self.save_percentages)
        self.save_button.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)

        self.grab_set()

    def save_percentages(self):
        try:
            train_percentage = float(self.train_entry.get())
            test_percentage = float(self.test_entry.get())
            validate_percentage = float(self.validate_entry.get())
        except ValueError:
            ErrorDialog(self, self.parent_window, "Percentages must be numbers.")
            return

        if train_percentage + test_percentage + validate_percentage != 100:
            ErrorDialog(self, self.parent_window, "Percentages must add up to 100.")
            return

        self.train_percentage = train_percentage
        self.test_percentage = test_percentage
        self.validate_percentage = validate_percentage

        self.destroy()

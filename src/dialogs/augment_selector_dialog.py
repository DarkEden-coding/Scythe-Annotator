import customtkinter as ctk


class AugmentSelectorDialog(ctk.CTkToplevel):
    def __init__(self, parent, augment_options, start_location=None):
        super().__init__(parent)
        self.geometry(f"500x400+{start_location[0] - 200}+{start_location[1] - 50}" if start_location else "500x400")
        self.title("Augment Selector")

        # Local variable to store selected augments
        self.selected_augments = []

        # Frames
        self.left_frame = ctk.CTkFrame(self, corner_radius=10)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ns")
        self.right_frame = ctk.CTkFrame(self, corner_radius=10)
        self.right_frame.grid(row=0, column=2, padx=10, pady=10, sticky="ns")
        self.control_frame = ctk.CTkFrame(self, corner_radius=10)
        self.control_frame.grid(row=0, column=1, padx=10, pady=10)

        # Labels
        self.left_label = ctk.CTkLabel(self.left_frame, text="Available Augments", font=("Arial", 16))
        self.left_label.pack(pady=5)
        self.right_label = ctk.CTkLabel(self.right_frame, text="Activated Augments", font=("Arial", 16))
        self.right_label.pack(pady=5)

        # Frames to hold augment buttons
        self.left_button_frame = ctk.CTkFrame(self.left_frame)
        self.left_button_frame.pack(pady=5, fill="both", expand=True)
        self.right_button_frame = ctk.CTkFrame(self.right_frame)
        self.right_button_frame.pack(pady=5, fill="both", expand=True)

        # Buttons for moving items
        self.move_right_btn = ctk.CTkButton(
            self.control_frame, text=">>", command=self.move_to_right, width=50
        )
        self.move_right_btn.grid(row=0, column=0, pady=10)
        self.move_left_btn = ctk.CTkButton(
            self.control_frame, text="<<", command=self.move_to_left, width=50
        )
        self.move_left_btn.grid(row=1, column=0, pady=10)

        # Add augment options as buttons
        self.left_buttons = []
        self.right_buttons = []
        for augment in augment_options:
            self.add_button(self.left_button_frame, augment, self.left_buttons)

        # Close button
        self.close_button = ctk.CTkButton(self, text="Close", command=self.on_close)
        self.close_button.grid(row=1, column=0, columnspan=3, pady=10)

        self.grab_set()

    def add_button(self, parent_frame, text, button_list):
        """Add a button to the specified frame and list."""
        button = ctk.CTkButton(parent_frame, text=text, command=lambda: self.select_button(button))
        button.pack(pady=2, fill="x")
        button_list.append(button)

    def select_button(self, button):
        """Highlight the selected button."""
        for btn in self.left_buttons + self.right_buttons:
            btn.configure(fg_color="transparent")  # Reset all buttons to default
        button.configure(fg_color="lightblue")  # Highlight the selected button
        self.selected_button = button

    def move_to_right(self):
        """Move the selected button to the right frame."""
        if hasattr(self, "selected_button") and self.selected_button in self.left_buttons:
            self.left_buttons.remove(self.selected_button)
            self.add_button(self.right_button_frame, self.selected_button.cget("text"), self.right_buttons)
            self.selected_button.destroy()
            del self.selected_button

    def move_to_left(self):
        """Move the selected button to the left frame."""
        if hasattr(self, "selected_button") and self.selected_button in self.right_buttons:
            self.right_buttons.remove(self.selected_button)
            self.add_button(self.left_button_frame, self.selected_button.cget("text"), self.left_buttons)
            self.selected_button.destroy()
            del self.selected_button

    def on_close(self):
        """Store the activated augments and close the window."""
        self.selected_augments = [btn.cget("text") for btn in self.right_buttons]
        self.destroy()

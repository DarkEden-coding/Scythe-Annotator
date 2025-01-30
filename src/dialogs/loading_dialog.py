from multiprocessing import Process

import customtkinter as ctk


class LoadingDialog:
    def __init__(self, display_text, start_location=None):
        self.process = Process(target=_LoadingDialog, args=(display_text, start_location))
        self.process.start()

    def close(self):
        self.process.terminate()
        self.process.join()


class _LoadingDialog(ctk.CTk):
    def __init__(self, display_text, start_location):
        """
        Display a progress dialog with a loading bar
        :param display_text: the text to display
        """
        super().__init__()
        self.title("Loading")
        self.geometry(f"300x100+{start_location[0] - 150}+{start_location[1] - 50}" if start_location else "300x100")

        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.loading_text = ctk.CTkLabel(self, text=display_text)
        self.loading_text.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self.loading = ctk.CTkProgressBar(self, orientation="horizontal", mode="indeterminate")
        self.loading.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

        self.loading.start()

        self.focus()
        self.mainloop()


if __name__ == "__main__":
    Process(target=LoadingDialog, args=("Loading", True)).start()

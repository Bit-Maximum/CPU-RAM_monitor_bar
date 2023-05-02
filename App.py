import tkinter as tk
from tkinter import ttk
import sys

# App GUI
class Aplication(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.set_window()
        self.set_ui()

    def set_window(self): # Начальные параметры окна
        self.attributes("-alpha", 1)
        self.attributes("-topmost", True)
        self.overrideredirect(True)
        self.resizable(False, False)
        self.title("CPU-RAM monitor")

    def set_ui(self): # Создание UI
        exit_btn = ttk.Button(self, text="Exit", command=self.app_exit)
        exit_btn.pack(fill=tk.X)

        self.bar2 = ttk.LabelFrame(self, text="Manual")
        self.bar2.pack(fill=tk.X)

        self.combo_win = ttk.Combobox(self.bar2, values=["hide", "don`t hide", "min"], state="readonly", width=10)
        self.combo_win.current(1) # Don`t Hide
        self.combo_win.pack(side=tk.LEFT)

        ttk.Button(self.bar2, text="Move").pack(side=tk.LEFT)
        ttk.Button(self.bar2, text=">>>").pack(side=tk.LEFT)

        self.bar2 = ttk.LabelFrame(self, text="Power")
        self.bar2.pack(fill=tk.BOTH)

        self.bind_class("Tk", "<Enter>", self.enter_mouse)
        self.bind_class("Tk", "<Leave>", self.leave_mouse)

    def enter_mouse(self, event):
        if self.combo_win.current() == 0 or 1:
            self.geometry("")

    def leave_mouse(self, event):
        if self.combo_win.current() == 0:
            self.geometry(f"{self.winfo_width()}x1")


    def app_exit(self):
        self.destroy()
        sys.exit()


if __name__ == "__main__":
    root = Aplication()
    root.mainloop()
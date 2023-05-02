import tkinter as tk
from tkinter import ttk
import sys
from process import CpuBar

# App GUI
class Aplication(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.set_window()
        self.set_ui()
        self.cpu = CpuBar()
        self.set_bar_cpu_usage()

    def set_window(self): # Начальные параметры окна
        self.attributes("-alpha", 1)
        self.attributes("-topmost", True)
        self.overrideredirect(True)
        self.resizable(False, False)
        self.title("CPU-RAM monitor")

    def set_ui(self): # Создание UI
        exit_btn = ttk.Button(self, text="Exit", command=self.app_exit)
        exit_btn.pack(fill=tk.X)

        self.bar_manual = ttk.LabelFrame(self, text="Manual")
        self.bar_manual.pack(fill=tk.X)

        self.combo_win = ttk.Combobox(self.bar_manual, values=["hide", "don`t hide", "min"], state="readonly", width=10)
        self.combo_win.current(1) # Don`t Hide
        self.combo_win.pack(side=tk.LEFT)

        ttk.Button(self.bar_manual, text="Move").pack(side=tk.LEFT)
        ttk.Button(self.bar_manual, text=">>>").pack(side=tk.LEFT)

        self.bar_power = ttk.LabelFrame(self, text="Power")
        self.bar_power.pack(fill=tk.BOTH)

        self.bind_class("Tk", "<Enter>", self.enter_mouse)
        self.bind_class("Tk", "<Leave>", self.leave_mouse)

    def set_bar_cpu_usage(self):
        ttk.Label(self.bar_power, text=f"physical cores: {self.cpu.cpu_count_physical}, logical cores: {self.cpu.cpu_count_logical}",anchor=tk.CENTER).pack(fill=tk.X)
        self.labels = []
        self.usage_bars = []
        for i in range(self.cpu.cpu_count_logical):
            self.labels.append(ttk.Label(self.bar_power, anchor=tk.CENTER))
            self.usage_bars.append(ttk.Progressbar(self.bar_power, length=100))
            self.labels[i].pack(fill=tk.X)
            self.usage_bars[i].pack(fill=tk.X)

    def enter_mouse(self, event):
        if self.combo_win.current() == 0 or 1:
            self.geometry("")

    def leave_mouse(self, event):
        if self.combo_win.current() == 0:
            self.geometry(f"{self.winfo_width()}x1")


    def app_exit(self):
        self.destroy()
        sys.exit()
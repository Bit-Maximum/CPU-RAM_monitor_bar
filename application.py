import tkinter as tk
from tkinter import ttk
import sys
from process import CpuBar
#from widget_update import Config_widgets

# App GUI
class Aplication(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.set_window()
        self.cpu = CpuBar()
        self.set_full_win()

    def set_full_win(self):
        self.set_ui()
        self.set_ram_usage()
        self.set_bar_cpu_usage()
        self.config_cpu_bars()
        self.config_ram_bar()

    def set_window(self): # Начальные параметры окна
        self.attributes("-alpha", 1)
        self.attributes("-topmost", True)
        self.overrideredirect(True)
        self.resizable(False, False)
        self.title("CPU-RAM monitor")

    def set_ui(self): # Создание UI
        self.bar_manual = ttk.LabelFrame(self, text="CPU-RAM monitor")
        self.bar_manual.pack(fill=tk.BOTH)

        self.combo_win = ttk.Combobox(self.bar_manual, values=["hide", "don`t hide", "min"], state="readonly", width=10)
        self.combo_win.current(1) # Don`t Hide
        self.combo_win.pack(side=tk.LEFT)

        ttk.Button(self.bar_manual, text="Move", command=self.move_win).pack(side=tk.LEFT)
        ttk.Button(self.bar_manual, text="Exit", command=self.app_exit).pack(side=tk.LEFT)

        self.bar_power = ttk.LabelFrame(self, text="Power")
        self.bar_power.pack(fill=tk.BOTH)

        self.bind_class("Tk", "<Enter>", self.enter_mouse)
        self.bind_class("Tk", "<Leave>", self.leave_mouse)
        self.combo_win.bind("<<ComboboxSelected>>", self.choise_combo_win)

    def set_bar_cpu_usage(self):
        ttk.Label(self.bar_power, text=f"physical cores: {self.cpu.cpu_count_physical}, logical cores: {self.cpu.cpu_count_logical}",anchor=tk.CENTER).pack(fill=tk.X)
        self.labels = []
        self.usage_bars = []
        for i in range(self.cpu.cpu_count_logical):
            self.labels.append(ttk.Label(self.bar_power, anchor=tk.CENTER))
            self.usage_bars.append(ttk.Progressbar(self.bar_power, length=100))
            self.labels[i].pack(fill=tk.X)
            self.usage_bars[i].pack(fill=tk.X)

    def set_ram_usage(self):
        self.ram_label = ttk.Label(self.bar_power, text="RAM usage: ", anchor=tk.CENTER)
        self.ram_label.pack(fill=tk.X)
        self.ram_bar = ttk.Progressbar(self.bar_power, length=100)
        self.ram_bar.pack(fill=tk.X)

    def change_to_full_win(self):
        self.after_cancel(self.wheel_minimalisic)
        self.clear_win()
        self.update()
        self.set_full_win()
        self.enter_mouse("")
        self.combo_win.current(1)

    def enter_mouse(self, event):
        if self.combo_win.current() == 0 or 1:
            self.geometry("")

    def leave_mouse(self, event):
        if self.combo_win.current() == 0:
            self.geometry(f"{self.winfo_width()}x1")

    def choise_combo_win(self, event):
        if self.combo_win.current() == 2:
            self.enter_mouse("")
            self.unbind_class('Tk', "<Enter>")
            self.unbind_class('Tk', "<Leave>")
            self.combo_win.unbind("<<ComboboxSelected>>")
            self.after_cancel(self.wheel_cpu)
            self.after_cancel(self.whell_ram)
            self.clear_win()
            self.update()
            self.set_minimalistic_win()

# Config Widgets
    def config_cpu_bars(self):
        cores = self.cpu.cpu_usage_procent()
        for i in range(self.cpu.cpu_count_logical):
            self.labels[i].configure(text=f"core {i + 1} usage: {cores[i]}%")
            self.usage_bars[i].configure(value=cores[i])
        self.wheel_cpu = self.after(1000, self.config_cpu_bars)

    def config_ram_bar(self):
        ram = self.cpu.ram_usage()
        self.ram_label.configure(text=f"RAM usage: {ram[2]}%, used {round(ram[3]/1048576)} Mb,\navalible: {round(ram[1]/1048576)} Mb")
        self.ram_bar.configure(value=ram[2])
        self.whell_ram = self.after(1000, self.config_ram_bar)

    def move_win(self):
        if self.wm_overrideredirect():
            self.overrideredirect(False)
        else:
            self.overrideredirect(True)
        self.update()

    def clear_win(self):
        for widget in self.winfo_children():
            widget.destroy()
    def app_exit(self):
        self.destroy()
        sys.exit()

# Minimalistic Style
    def set_minimalistic_win(self):
        self.bar_mini_info = ttk.Label(self, text="")
        self.bar_mini_info.pack(fill=tk.BOTH)
        self.mini_label = ttk.Label(self.bar_mini_info, text="      CPU usage:        RAM usage: {ram[2]}%", anchor=tk.W)
        self.mini_label.pack(fill=tk.X)

        self.bar_cpu_mini = ttk.Progressbar(self, length=100)
        self.bar_cpu_mini.pack(side=tk.LEFT)

        self.bar_ram_mini = ttk.Progressbar(self, length=100)
        self.bar_ram_mini.pack(side=tk.LEFT)

        ttk.Button(self, text="Full", width=5, command=self.change_to_full_win).pack(side=tk.RIGHT)
        ttk.Button(self, text="Move", width=5, command=self.move_win).pack(side=tk.RIGHT)

        self.update()
        self.config_minimalistic_win()

    def config_minimalistic_win(self):
        cpu_percent = self.cpu.cpu_usage_mini()
        ram_percent = self.cpu.ram_usage()[2]
        self.mini_label.configure(
            text=f"       CPU: {cpu_percent}%               RAM: {ram_percent}%")

        self.bar_cpu_mini.configure(value=cpu_percent)
        self.bar_ram_mini.configure(value=ram_percent)

        self.wheel_minimalisic = self.after(1000, self.config_minimalistic_win)

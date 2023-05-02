import psutil as pt


class CpuBar:
    def __init__(self):
        self.cpu_count_physical = pt.cpu_count(logical=False)
        self.cpu_count_logical = pt.cpu_count(logical=True)

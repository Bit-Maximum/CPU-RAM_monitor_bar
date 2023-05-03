import psutil as pt


class CpuBar:
    def __init__(self):
        self.cpu_count_physical = pt.cpu_count(logical=False)
        self.cpu_count_logical = pt.cpu_count(logical=True)

    def cpu_usage_procent(self):
        return pt.cpu_percent(percpu=True)

    def cpu_usage_mini(self):
        return pt.cpu_percent()

    def ram_usage(self):
        return pt.virtual_memory()
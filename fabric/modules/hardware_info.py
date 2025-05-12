from imports import *

from fabricators import psutil_fabricator, amdgpu_top_fabricator, cache_fabricator


class HardwareInfo(Box):
    def __init__(self):
        for label in [
            "cpu_usage",
            "cpu_temp",
            "gpu_usage",
            "gpu_temp",
            "disk_usage",
            "ram_usage",
        ]:
            setattr(
                self, label, Label(label="N/A", h_expand=True, name="hardware-label")
            )

        for icon in ["cpu_icon", "gpu_icon", "ram_icon", "cache_icon"]:
            setattr(
                self,
                icon,
                Image(
                    icon_name=getattr(Config, icon),
                    icon_size=Config.icon_size,
                    name="icon",
                ),
            )

        self.cache_label = Label(h_expand=True, name="cache-label")

        self.network_label = Label(h_expand=True, name="revealer-label")

        self.network_icon_stack = Stack(transition_type="slide-up-down")
        for status in [
            "network-wired-acquiring",
            "network-wired",
            "network-wired-disconnected",
        ]:
            self.network_icon_stack.add_named(
                Image(
                    icon_name=f"{status}-symbolic",
                    icon_size=Config.icon_size,
                    name="icon",
                ),
                name=status,
            )

        super().__init__(
            orientation="v",
            children=[
                Box(
                    v_expand=True,
                    children=[
                        self.cpu_usage,
                        self.cpu_icon,
                        self.cpu_temp,
                    ],
                ),
                Box(
                    v_expand=True,
                    children=[
                        self.gpu_usage,
                        self.gpu_icon,
                        self.gpu_temp,
                    ],
                ),
                Box(v_expand=True, children=[self.ram_icon, self.ram_usage]),
                Box(v_expand=True, children=[self.cache_icon, self.cache_label]),
                Box(
                    v_expand=True,
                    children=[self.network_icon_stack, self.network_label],
                ),
            ],
        )
        psutil_fabricator.connect("changed", self.label_handler)
        amdgpu_top_fabricator.connect("changed", self.gpu_label_handler)
        cache_fabricator.connect("changed", self.cache_label_handler)

    def label_handler(self, fabricator, value):
        if value["is_network_up"]:
            self.network_label.set_label(value["ip_address"])
            self.network_icon_stack.set_visible_child_name("network-wired")
        else:
            self.network_label.set_label("N/A")
            self.network_icon_stack.set_visible_child_name("network-wired-disconnected")

        for k, v in {
            self.cpu_usage: "cpu_usage",
            self.cpu_temp: "cpu_temp",
            self.disk_usage: "disk_usage",
            self.ram_usage: "ram_usage",
        }.items():
            k.set_label(value[v])

    def cache_label_handler(self, fabricator, value):
        self.cache_label.set_label(self.convert_kb_to_gb(int(value.split()[1])))

    def gpu_label_handler(self, fabricator, value):
        data = json.loads(value)[0]
        self.gpu_temp.set_label(f"{data['Sensors']['Junction Temperature']['value']}°C")
        self.gpu_usage.set_label(f"{data['gpu_activity']['GFX']['value']}%")

    @staticmethod
    def convert_kb_to_gb(number):
        return (
            f"{round(number / 1048576, 1)} GB"
            if number >= 1048576
            else f"{round(number / 1024, 1)} MB"
            if number >= 1024
            else f"{number} KB"
        )

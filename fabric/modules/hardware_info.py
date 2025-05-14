from imports import *

from fabricators import psutil_fabricator, amdgpu_top_fabricator, cache_fabricator


class HardwareInfo(Box):
    def __init__(self):
        for item in [
            "cpu",
            "gpu",
            "disk",
            "ram",
        ]:
            setattr(
                self,
                f"{item}_usage",
                CircularProgressBar(
                    line_width=2,
                    start_angle=-90,
                    size=25,
                    child=Image(
                        icon_name=getattr(Config, f"{item}_icon"),
                        icon_size=Config.icon_size - 5,
                        style_classes="icon",
                    ),
                    max_value=100,
                    name="circular-progress",
                ),
            )

        self.cache_icon = Image(
            icon_name=Config.cache_icon,
            icon_size=Config.icon_size,
            h_expand=True,
            name="icon",
        )

        self.cache_label = Label(h_expand=True, name="cache-label")

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
        self.network_icon_button = Button(
            child=self.network_icon_stack,
            style_classes="cool-button",
            # TODO on_clicked=
        )

        super().__init__(
            orientation="v",
            spacing=10,
            children=[
                Box(v_expand=True, children=[self.cache_icon, self.cache_label]),
                CenterBox(
                    start_children=self.cpu_usage,
                    center_children=self.ram_usage,
                    end_children=self.gpu_usage,
                ),
            ],
        )
        psutil_fabricator.connect("changed", self.label_handler)
        amdgpu_top_fabricator.connect("changed", self.gpu_label_handler)
        cache_fabricator.connect("changed", self.cache_label_handler)

    def label_handler(self, fabricator, value):
        if value["is_network_up"]:
            self.network_icon_stack.set_tooltip_text(value["ip_address"])
            self.network_icon_stack.set_visible_child_name("network-wired")
        else:
            self.network_icon_stack.set_tooltip_text("N/A")
            self.network_icon_stack.set_visible_child_name("network-wired-disconnected")

        for k, v in {
            self.cpu_usage: "cpu_usage",
            self.disk_usage: "disk_usage",
            self.ram_usage: "ram_usage",
        }.items():
            k.set_value(value[v])

    def cache_label_handler(self, fabricator, value):
        self.cache_label.set_label(self.convert_kb_to_gb(int(value.split()[1])))

    def gpu_label_handler(self, fabricator, value):
        data = json.loads(value)[0]

        self.gpu_usage.set_value(data["gpu_activity"]["GFX"]["value"])

    @staticmethod
    def convert_kb_to_gb(number):
        return (
            f"{round(number / 1048576, 1)} GB"
            if number >= 1048576
            else f"{round(number / 1024, 1)} MB"
            if number >= 1024
            else f"{number} KB"
        )

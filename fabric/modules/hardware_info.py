from imports import *

from fabricators import psutil_fabricator, cache_fabricator


class NetworkInfo(Button):
    def __init__(self):
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
            child=self.network_icon_stack,
            style_classes="cool-button",
            # TODO on_clicked=
        )
        psutil_fabricator.connect("changed", self.label_handler)

    def label_handler(self, fabricator, value):
        if value["is_network_up"]:
            self.network_icon_stack.set_tooltip_text(value["ip_address"])
            self.network_icon_stack.set_visible_child_name("network-wired")
        else:
            self.network_icon_stack.set_tooltip_text("N/A")
            self.network_icon_stack.set_visible_child_name("network-wired-disconnected")


class StorageInfo(Box):
    def __init__(self):
        self.cache_icon = Image(
            icon_name=Config.cache_icon,
            icon_size=Config.icon_size,
            name="icon",
        )

        self.cache_label = Label(h_expand=True, name="cache-label")

        super().__init__(children=[self.cache_icon, self.cache_label])

        cache_fabricator.connect("changed", self.cache_label_handler)

    def cache_label_handler(self, fabricator, value):
        self.cache_label.set_label(self.convert_kb_to_gb(int(value.split()[1])))

    @staticmethod
    def convert_kb_to_gb(number):
        return (
            f"{round(number / 1048576, 1)} GB"
            if number >= 1048576
            else f"{round(number / 1024, 1)} MB"
            if number >= 1024
            else f"{number} KB"
        )

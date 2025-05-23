from config import Config
from fabricators import device_fabricator
from imports import *


class RemoveDevice(WaylandWindow):
    def __init__(self):
        self.grid = Gtk.Grid(visible=True)
        self.box = Box(children=self.grid)
        super().__init__(
            visible=True, anchor="top right", title="remove-device", child=self.box
        )
        device_fabricator.connect("changed", self.join_json)
        self.ugly_json = ""
        self.handsome_json = []

    def join_json(self, fabricator, value):
        self.ugly_json += value
        try:
            self.format_json(loads(self.ugly_json))
        except JSONDecodeError:
            pass

    def format_json(self, json_to_format):
        def extract_children(parent_to_iterate):
            for disk in parent_to_iterate:
                for key, value in disk.items():
                    # iterate through childen, which contain partition info
                    if isinstance(value, list):
                        extract_children(value)

                # yeet the disks/partitions with no filesystem
                if disk["fstype"] is not None:
                    self.handsome_json.append(disk)

        extract_children(json_to_format["blockdevices"])

        self.create_grid()

    def create_grid(self):
        for title in Config.shown_info:
            if Config.shown_info[title]:
                self.grid.attach(
                    Label(label=Config.pretty_names[title], name="disk-titles"),
                    [key for key, value in Config.shown_info.items() if value].index(
                        title
                    ),
                    0,
                    1,
                    1,
                )

        for disk in self.handsome_json:
            column = 0
            for key, value in disk.items():
                if Config.shown_info[key]:
                    self.grid.attach(
                        Label(
                            label=value,
                            tooltip_text="\n".join(self.hidden_props(disk)),
                        ),
                        column,
                        self.handsome_json.index(disk) + 1,
                        1,
                        1,
                    )

                    column += 1

    def hidden_props(self, disk):
        return [
            f"{Config.pretty_names[key]}: {value}"
            for key, value in disk.items()
            if not Config.shown_info[key] and value is not None
        ]

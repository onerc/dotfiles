from fabricators import device_fabricator
from imports import *


class RemoveDevice(WaylandWindow):
    def __init__(self):
        self.box = Box(orientation="v")
        super().__init__(
            anchor="top right",
            child=self.box,
            monitor=Config.favorite_monitor_index,
            title="remove-device",
            visible=True,
        )
        device_fabricator.connect("changed", self.check_if_different)
        self.old_json = []
        self.formatted_json = []

    def check_if_different(self, fabricator, value):
        if self.old_json != value:
            self.old_json = value
            self.its_rewind_time()
            self.format_json(value)

    def its_rewind_time(self):
        self.formatted_json.clear()
        for child in self.box.get_children():
            child.destroy()

    def format_json(self, json_to_format):
        def extract_children(parent_to_iterate):
            for disk in parent_to_iterate:
                # convert vfat to fat*
                if disk["fstype"] == "vfat":
                    disk.update(fstype=disk["fsver"].lower())

                # yeet the disks/partitions with no filesystem
                if disk["fstype"] is not None:
                    self.formatted_json.append(disk)

                # iterate through childen, which contain partition info
                for value in disk.values():
                    if isinstance(value, list):
                        extract_children(value)

        extract_children(loads(json_to_format)["blockdevices"])
        self.create_grid()

    def create_grid(self):
        for disk in self.formatted_json:
            for key in disk.keys():
                if Config.shown_info[key]:
                    self.box.add(
                        Button(
                            style_classes="cool-button",
                            tooltip_text="\n".join(self.hidden_props(disk)),
                            child=Box(children=self.visible_props(disk)),
                            on_clicked=lambda *args,
                            value=disk: exec_shell_command_async(
                                f"udisksctl {'unmount' if value['mountpoint'] else 'mount'} -b /dev/{value['name']}"
                            ),
                        )
                    )
                    break

    def hidden_props(self, disk):
        # iterate through the ones hidden in the config, ignore fsver, strip None and capitalize abbreviations
        return [
            f"{Config.pretty_names[key]}: {self.abbreviation_capitalizer(value) if key in ['tran', 'pttype'] else value}"
            for key, value in disk.items()
            if not Config.shown_info[key] and key != "fsver" and value is not None
        ]

    def visible_props(self, disk):
        return [
            Label(
                label=disk[k] if disk[k] else "•",
                style_classes="device-label"
                if disk["mountpoint"]
                else ["device-label", "passive"],
            )
            for k, v in Config.shown_info.items()
            if v
        ]

    @staticmethod
    def abbreviation_capitalizer(abbreviation):
        # fk you nvme
        return "NVMe" if abbreviation == "nvme" else abbreviation.upper()

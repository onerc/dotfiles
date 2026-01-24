from fabricators import device_fabricator, cache_fabricator
from imports import *


class RemoveDevicePopUp(WaylandWindow):
    def __init__(self):
        self.visible_props = [
            prop
            for prop in list(config.info.__dict__)
            if getattr(config.info, prop).show
        ]
        self.cache_label = Label(h_expand=True, name="cache-label")
        self.title_box = Box(
            children=[
                Label(label=getattr(config.info, prop).pretty_name, name="disk-titles")
                for prop in self.visible_props
            ]
        )
        self.big_box = Box(
            children=[self.cache_label, self.title_box],
            orientation="v",
        )
        self.cache_json = []
        self.formatted_json = []

        super().__init__(
            anchor="top right",
            child=self.big_box,
            monitor=config.hardware.favorite_monitor_index,
            title="remove-device",
            visible=False,
        )
        device_fabricator.connect("changed", self.check_if_different)
        cache_fabricator.connect("changed", self.cache_label_handler)

    def cache_label_handler(self, fabricator, value):
        self.cache_label.set_label(self.convert_kb_to_gb(int(value.split()[1])))

    def check_if_different(self, fabricator, value):
        if self.cache_json != value:
            self.cache_json = value
            self.clear_lines()
            self.format_json(loads(value)["blockdevices"])
            self.create_disk_info_lines()

    def clear_lines(self):
        self.formatted_json.clear()
        utils.destroy_useless_children(self.big_box, 2)

    def format_json(self, json_to_format):
        for disk in json_to_format:
            # convert vfat to fat*
            if disk["fstype"] == "vfat":
                disk.update(fstype=disk["fsver"].lower())

            # yeet the disks/partitions with no filesystem
            if disk["fstype"] is not None:
                self.formatted_json.append(disk)

            # iterate through childen, which contain partition info
            for children in disk.values():
                if isinstance(children, list):
                    self.format_json(children)
                    # for some reason, nvme partitions inherit their interface from parents but sata partitions dont
                    # may be a problem with ntfs, idk
                    for child in children:
                        child.update(tran=disk["tran"])

    def create_disk_info_lines(self):
        for disk in self.formatted_json:
            for key in disk.keys():
                if getattr(config.info, key).show:
                    self.big_box.add(
                        Button(
                            style_classes="cool-button",
                            tooltip_text="\n".join(
                                self.set_hidden_props_as_tooltip(disk)
                            ),
                            child=Box(children=self.populate_visible_props(disk)),
                            on_clicked=lambda *args,
                            value=disk: exec_shell_command_async(
                                f"udisksctl {'unmount' if value['mountpoint'] else 'mount'} -b /dev/{value['name']}"
                            ),
                        )
                    )
                    break

    def set_hidden_props_as_tooltip(self, disk):
        # iterate through the ones hidden in the config, ignore fsver key and None value, capitalize abbreviations
        return [
            f"{getattr(config.info, key).pretty_name}: {self.abbreviation_capitalizer(value) if key in ['tran', 'pttype'] else value}"
            for key, value in disk.items()
            if not getattr(config.info, key).show
            and key != "fsver"
            and value is not None
        ]

    def populate_visible_props(self, disk):
        return [
            Label(
                label=disk[prop] if disk[prop] else "•",
                style_classes="device-label"
                if disk["mountpoint"]
                else ["device-label", "passive"],
            )
            for prop in self.visible_props
        ]

    @staticmethod
    def abbreviation_capitalizer(abbreviation: str) -> str:
        # fk you nvme
        return "NVMe" if abbreviation == "nvme" else abbreviation.upper()

    @staticmethod
    def convert_kb_to_gb(number: int) -> str:
        return (
            f"{round(number / 1048576, 1)} GB"
            if number >= 1048576
            else f"{round(number / 1024, 1)} MB"
            if number >= 1024
            else f"{number} KB"
        )


remove_device = RemoveDevicePopUp()


class ToggleRemoveDeviceVisibility(Button):
    def __init__(self):
        super().__init__(
            child=Image(
                icon_name=config.icons.cache_icon,
                icon_size=config.eye_candy.icon_size,
                name="icon",
            ),
            style_classes="cool-button",
            on_clicked=lambda *args: utils.toggle_visibility(remove_device),
        )

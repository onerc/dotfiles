from imports import *


class Config:
    pretty_names: dict = {
        "name": "Name",
        "size": "Capacity",
        "fsused": "Used",
        "fstype": "FS",
        "fsver": "FS Version",
        "label": "Label",
        "mountpoint": "Mount Point",
        "tran": "Interface",
        "pttype": "Partition Table",
        "model": "Model",
        "parttypename": "Partition Type",
    }
    shown_info: dict = {
        "name": True,
        "size": True,
        "fsused": True,
        "fstype": True,
        "fsver": False,
        "label": True,
        "mountpoint": False,
        "tran": False,
        "pttype": False,
        "model": False,
        "parttypename": False,
    }

    # window manager
    number_of_workspaces: int = 10

    # hardware
    favorite_monitor_index: int = 0
    network_interface: str = "enp6s0"

    # icons
    cpu_icon: str = "cpu-symbolic"
    gpu_icon: str = "freon-gpu-temperature-symbolic"
    disk_icon: str = "drive-harddisk-system-symbolic"
    ram_icon: str = "ram-symbolic"
    cache_icon: str = "drive-removable-media-symbolic"
    headphone_icon: str = "audio-headphones"
    speaker_icon: str = "video-display"
    unwanted_sink_icon: str = "dialog-error"

    # eye candy
    transition_duration: int = 250
    icon_size: int = 16
    calendar_button_size: int = 16
    suppress_logger: bool = True

    # audio
    speaker_volume_increment: int = 10
    microphone_volume_increment: int = 10
    speaker_name: str = "alsa_output.pci-0000_03_00.1.hdmi-stereo"
    headphones_name: str = "alsa_output.pci-0000_00_1f.3.analog-stereo"
    unwanted_sink: str = "alsa_output.pci-0000_00_1f.3.iec958-stereo"


if Config.suppress_logger:
    logger.remove()

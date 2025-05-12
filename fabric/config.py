from imports import *


class Config:
    # window manager
    number_of_workspaces: int = 10

    # hardware
    favorite_monitor_index: int = 0
    network_interface: str = "enp6s0"
    psutil_cpu: str = "coretemp"
    psutil_gpu: str = "amdgpu"

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
    speaker_name: str = "alsa_output.pci-0000_03_00.1.hdmi-stereo"
    headphones_name: str = "alsa_output.pci-0000_00_1f.3.analog-stereo"
    unwanted_sink: str = "alsa_output.pci-0000_00_1f.3.iec958-stereo"


if Config.suppress_logger:
    logger.remove()

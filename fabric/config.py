from loguru import logger


class Config:
    # weather
    api_key = "d07186c0c823985f93cf8b2b1dc0c387"
    city_name = ""

    # hardware
    network_interface = "enp6s0"
    psutil_cpu = "coretemp"
    psutil_gpu = "amdgpu"

    # icons
    cpu_icon = "cpu-symbolic"
    gpu_icon = "freon-gpu-temperature-symbolic"
    disk_icon = "drive-harddisk-system-symbolic"
    ram_icon = "ram-symbolic"
    cache_icon = "drive-removable-media-symbolic"
    headphone_icon = "audio-headphones"
    speaker_icon = "video-display"
    unwanted_sink_icon = "dialog-error"

    # eye candy
    transition_duration = 250
    icon_size = 16
    calendar_button_size = 16
    suppress_logger = True

    # audio
    speaker_name = "alsa_output.pci-0000_03_00.1.hdmi-stereo"
    headphones_name = "alsa_output.pci-0000_00_1f.3.analog-stereo"
    unwanted_sink = "alsa_output.pci-0000_00_1f.3.iec958-stereo"


if Config.suppress_logger:
    logger.remove()

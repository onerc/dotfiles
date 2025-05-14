from imports import *


def psutil_poll(fabricator):
    while True:
        yield {
            "cpu_usage": round(psutil.cpu_percent()),
            "ram_usage": round(psutil.virtual_memory().percent),
            "disk_usage": round(psutil.disk_usage("/").percent),
            # "cpu_temp": f"{round(psutil.sensors_temperatures()[Config.psutil_cpu][0].current)}°C",
            # "gpu_temp": f"{round(psutil.sensors_temperatures()[config["psutil_gpu"]][1].current)}°C",
            "is_network_up": psutil.net_if_stats()[Config.network_interface].isup,
            "ip_address": psutil.net_if_addrs()[Config.network_interface][0].address,
        }
        sleep(1)


psutil_fabricator = Fabricator(poll_from=psutil_poll, stream=True)
amdgpu_top_fabricator = Fabricator(poll_from="amdgpu_top -d -J", interval=1000)
cache_fabricator = Fabricator(poll_from="grep Dirty: /proc/meminfo", interval=1000)
now_playing_fabricator = Fabricator(
    poll_from=r"playerctl -F metadata --format '{{status}}\n{{album}}\n{{artist}}\n{{position}}\n{{title}}\n{{volume}}\n{{playerName}}'",
    stream=True,
)

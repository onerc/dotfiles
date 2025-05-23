from imports import *


def psutil_poll(fabricator):
    while True:
        yield {
            "is_network_up": psutil.net_if_stats()[Config.network_interface].isup,
            "ip_address": psutil.net_if_addrs()[Config.network_interface][0].address,
        }
        sleep(1)


psutil_fabricator = Fabricator(poll_from=psutil_poll, stream=True)
cache_fabricator = Fabricator(poll_from="grep Dirty: /proc/meminfo")

device_fabricator = Fabricator(
    poll_from="lsblk -Jo NAME,SIZE,FSUSED,FSTYPE,FSVER,LABEL,MOUNTPOINT,TRAN,PTTYPE,MODEL,PARTTYPENAME",
)
now_playing_fabricator = Fabricator(
    poll_from=r"playerctl -F metadata --format '{{status}}\n{{album}}\n{{artist}}\n{{position}}\n{{title}}\n{{volume}}\n{{playerName}}'",
    stream=True,
)

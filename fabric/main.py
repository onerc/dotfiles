from fabric.utils import monitor_file
from modules.audio import SpeakerVolume, MicVolume, AudioOutputSwitch
from modules.now_playing import NowPlaying, OldNowPlaying
from modules.power import Power
from modules.hardware_info import NetworkInfo

from modules.remove_device import ToggleRemoveDeviceVisibility
from overrides import OverriddenDateTime, OverriddenWorkspaces
from imports import *

# imported so they are accessible with cli
from modules.app_launcher import app_launcher
from modules.calendar import calendar
from modules.remove_device import remove_device


class barbar(WaylandWindow):
    def __init__(self):
        super().__init__(
            anchor="left top right",
            exclusivity="auto",
            monitor=config.hardware.favorite_monitor_index,
            visible=False,
        )

        self.centerbox = CenterBox(
            start_children=OverriddenWorkspaces(),
            center_children=Box(
                children=[
                    NetworkInfo(),
                    OverriddenDateTime(),
                    AudioOutputSwitch(),
                ]
            ),
            end_children=[
                OldNowPlaying(),
                ToggleRemoveDeviceVisibility(),
                MicVolume(),
                SpeakerVolume(),
                Power(),
            ],
        )

        self.add(self.centerbox)
        self.show_all()


if __name__ == "__main__":
    bar = Application(window=barbar(), open_inspector=True)
    bar.style_monitor = monitor_file(get_relative_path("style.css"))
    bar.style_monitor.connect(
        "changed",
        lambda *args: bar.set_stylesheet_from_file(
            file_path=get_relative_path("style.css")
        ),
    )
    bar.set_stylesheet_from_file(file_path=get_relative_path("style.css"))

    bar.run()

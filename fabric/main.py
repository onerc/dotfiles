from modules.audio import SpeakerVolume, MicVolume, AudioOutputSwitch
from modules.now_playing import NowPlaying
from modules.power import Power
from modules.hardware_info import HardwareInfo

from overrides import OverriddenDateTime, OverriddenWorkspaces
from imports import *

# imported so they are accessible with cli
from modules.app_launcher import app_launcher
from modules.calendar import calendar_pop_up


class barbar(WaylandWindow):
    def __init__(self):
        super().__init__(
            anchor="left top right",
            exclusivity="auto",
            monitor=Config.favorite_monitor_index,
            visible=False,
        )

        self.centerbox = CenterBox(
            start_children=OverriddenWorkspaces(),
            center_children=NowPlaying(),
            end_children=[
                AudioOutputSwitch(),
                MicVolume(),
                SpeakerVolume(),
                HardwareInfo().network_icon_button,
                Power(),
                OverriddenDateTime(),
            ],
        )
        self.add(self.centerbox)
        self.show_all()


if __name__ == "__main__":
    bar = Application(barbar(), open_inspector=False)
    bar.set_stylesheet_from_file(
        file_path=get_relative_path("so_styling_much_wow/style.css")
    )
    bar.run()

from modules.audio import SpeakerVolume, MicVolume, AudioOutputSwitch
from modules.nowplaying import NowPlaying
from modules.power import Power

from overrides import OverriddenDateTime, OverriddenWorkspaces
from imports import *

from modules.app_launcher import app_launcher
from modules.pop_up import pop_up


class barbar(WaylandWindow):
    def __init__(self):
        super().__init__(
            layer="top",
            anchor="left top right",
            exclusivity="auto",
            visible=False,
            monitor=0,
        )

        self.centerbox = CenterBox(
            start_children=OverriddenWorkspaces(),
            center_children=OverriddenDateTime(),
            end_children=Box(
                children=[
                    NowPlaying(),
                    AudioOutputSwitch(),
                    MicVolume(),
                    SpeakerVolume(),
                    Power(),
                ]
            ),
        )
        self.add(self.centerbox)
        self.show_all()


if __name__ == "__main__":
    bar = Application(barbar(), open_inspector=True)
    bar.set_stylesheet_from_file(
        file_path=get_relative_path("so_styling_much_wow/style.css")
    )
    bar.run()

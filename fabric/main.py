from modules.audio import SpeakerVolume, MicVolume, AudioOutputSwitch
from modules.nowplaying import NowPlaying
from modules.overrides import OverriddenDateTime, OverriddenWorkspaces
from modules.power import Power
from modules.popup import pop_up
from modules.applauncher import app_launcher
from imports import *


class barbar(WaylandWindow):
    def __init__(self):
        super().__init__(
            layer="top",
            anchor="left top right",
            exclusivity="auto",
            visible=False,
            monitor=0,
        )

        self.media = Box(
            children=[
                NowPlaying(),
                AudioOutputSwitch(),
                MicVolume(),
                SpeakerVolume(),
                Power(),
            ]
        )
        self.centerbox = CenterBox(
            start_children=OverriddenWorkspaces(),
            center_children=OverriddenDateTime(),
            end_children=self.media,
        )

        self.add(self.centerbox)
        self.show_all()


def window_focus(action):
    match action:
        case "show":
            pop_up.set_keyboard_mode("exclusive")
            app_launcher.entry.grab_focus()
            pop_up.show()
        case "hide":
            pop_up.set_keyboard_mode("on-demand")
            app_launcher.entry.grab_remove()
            pop_up.hide()


if __name__ == "__main__":
    bar = Application(barbar(), open_inspector=True)
    bar.set_stylesheet_from_file(
        file_path=get_relative_path("so_styling_much_wow/style.css")
    )
    bar.run()

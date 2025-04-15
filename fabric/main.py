from modules.start.overridden_workspaces import OverriddenWorkspaces

from modules.center.middle_stack import middle_stack
from modules.center.pop_up import pop_up

from modules.end.audio import SpeakerVolume, MicVolume, AudioOutputSwitch
from modules.end.nowplaying import NowPlaying
from modules.end.power import Power

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

        self.centerbox = CenterBox(
            start_children=OverriddenWorkspaces(),
            center_children=middle_stack,
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

    def window_focus(self, action):
        match action:
            case "show":
                self.set_keyboard_mode("exclusive")
                middle_stack.set_visible_child_name("app_launcher")
                middle_stack.app_launcher.entry.grab_focus()
            case "hide":
                self.set_keyboard_mode("none")
                middle_stack.set_visible_child_name("date_time")
                if pop_up.get_visible():
                    pop_up.hide()


the_bar = barbar()


if __name__ == "__main__":
    bar = Application(the_bar, open_inspector=False)
    bar.set_stylesheet_from_file(
        file_path=get_relative_path("so_styling_much_wow/style.css")
    )
    bar.run()

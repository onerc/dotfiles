from imports import *
from config import Config


# from modules.owm_weather import WeatherGrid
from modules.hardwareinfo import HardwareInfo

from modules.applauncher import app_launcher


class PopUpStack(Box):
    def __init__(self):
        self.stack = Stack(
            transition_duration=Config.transition_duration,
            transition_type="slide-left-right",
        )

        self.stack.add_titled(
            Button(label="hello im a button"),
            # ScrolledWindow(
            #     # on_grab_notify=lambda *args: print("a"),
            #     style_classes="scrolly",
            #     kinetic_scroll=True,
            #     child=Box(
            #         children=[
            #             Button(
            #                 label=f"{app.executable}",
            #                 on_clicked=lambda *args, value=app: value.launch(),
            #             )
            #         ]
            #     ),
            # ),
            name="weather",
            title="Weather",
        )

        self.stack.add_titled(
            HardwareInfo(),
            name="stats",
            title="Stats",
        )

        self.stack_switcher = Gtk.StackSwitcher(visible=True)
        self.stack_switcher.set_stack(self.stack)

        for button in self.stack_switcher.get_children():
            button.set_hexpand(True)
            button.set_name("stack_switcher")
        super().__init__(
            orientation="v",
            children=[self.stack_switcher, self.stack],
        )


class PopUp(WaylandWindow):
    def __init__(self):
        super().__init__(
            anchor="top right",
            visible=False,
            child=Box(orientation="v", children=[PopUpStack(), app_launcher]),
            keyboard_mode="on-demand",
        )


pop_up = PopUp()


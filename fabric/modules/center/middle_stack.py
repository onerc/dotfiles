from imports import *
from config import Config

from modules.center.pop_up import pop_up


class OverriddenDateTime(DateTime):
    def __init__(self):
        super().__init__(formatters="%H:%M", style_classes="cool-button")

    def do_handle_press(self, _, event, *args):
        if event.button == 1:
            pop_up.hide() if pop_up.get_visible() else pop_up.show()


class AppLauncher(Overlay):
    def __init__(self):
        self.app_list = [
            PurePath(f"{app.executable}").name  # stripping paths
            for app in get_desktop_applications(include_hidden=True)
        ]

        self.ghost_entry = Entry()
        self.ghost_entry.set_property("xalign", 1)
        self.entry = Entry(
            notify_text=lambda entry, *args: self.fuzzy_match(entry.get_text()),
            on_activate=self.on_activate,
            style_classes="app_launcher",
        )
        super().__init__(
            child=self.ghost_entry,
            overlays=self.entry,
        )

    def fuzzy_match(self, entry):
        self.ghost_entry.set_placeholder_text(
            process.extractOne(query=entry, choices=self.app_list)[0] if entry else ""
        )

    def on_activate(self, entry):
        Hyprland.send_command(
            f"dispatch exec {self.ghost_entry.get_placeholder_text()}"
        )
        self.entry.delete_text(0, -1)

        exec_shell_command_async(
            "python -m fabric execute default \"the_bar.window_focus('hide')\""
        )


class MiddleStack(Stack):
    def __init__(self):
        self.app_launcher = AppLauncher()
        self.overridden_datetime = OverriddenDateTime()
        super().__init__(
            transition_duration=Config.transition_duration,
            transition_type="slide-up-down",
        )
        self.add_named(self.overridden_datetime, name="date_time")
        self.add_named(self.app_launcher, name="app_launcher")


middle_stack = MiddleStack()

from imports import *


class AppLauncherPopUp(WaylandWindow):
    def __init__(self):
        self.app_list = [
            PurePath(f"{app.executable}").name  # stripping paths
            for app in get_desktop_applications(include_hidden=True)
        ]

        self.ghost_entry = Entry()
        self.ghost_entry.set_property("xalign", 1)
        # Prevents being able to Tab or Shift-Tab to ghost_entry and avoids the need of grabbing focus to actual entry
        self.ghost_entry.set_property("can_focus", False)
        self.entry = Entry(
            notify_text=lambda entry, *args: self.fuzzy_match(entry.get_text()),
            on_activate=self.on_activate,
            name="app-launcher-entry",
        )
        super().__init__(
            anchor="top center",
            child=Overlay(
                child=self.ghost_entry,
                overlays=self.entry,
            ),
            keyboard_mode="exclusive",
            monitor=Config.favorite_monitor_index,
            name="app-launcher-window",
            title="app-launcher",
            visible=False,
        )

    def fuzzy_match(self, entry):
        self.ghost_entry.set_placeholder_text(
            process.extractOne(query=entry, choices=self.app_list)[0] if entry else ""
        )

    def on_activate(self, entry):
        Hyprland.send_command(
            f"dispatch exec {self.ghost_entry.get_placeholder_text()}"
        )
        self.clear_and_hide()

    def clear_and_hide(self):
        self.entry.delete_text(0, -1)
        self.hide()


app_launcher = AppLauncherPopUp()

from imports import *


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

        # FIXME
        from main import window_focus

        window_focus("hide")


app_launcher = AppLauncher()


# on_focus_in_event=lambda *args: self.entry.set_buffer(
#     Gtk.EntryBuffer(text=match[0])
# ),

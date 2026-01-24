from imports import *


class AppLauncherPopUp(WaylandWindow):
    def __init__(self):
        self.app_list = sorted(
            set(
                PurePath(f"{app.executable}").name  # stripping paths
                for app in get_desktop_applications()
            ),
            key=str.lower,
        )

        self.matchbox = Box(orientation="v", name="app-launcher-box")
        self.entry = Entry(
            notify_text=lambda entry, *args: self.populate_matchbox(entry.get_text()),
            on_activate=lambda *args: self.run_the_match(),
            name="app-launcher-entry",
        )

        super().__init__(
            anchor="top center",
            child=Box(orientation="v", children=[self.entry, self.matchbox]),
            keyboard_mode="on-demand",
            monitor=config.hardware.favorite_monitor_index,
            name="app-launcher-window",
            title="app-launcher",
            visible=False,
        )

    @staticmethod
    def create_and_style_label(entry, word_to_match):
        markup = ""
        for code, entry_start, entry_stop, wtm_start, wtm_stop in SequenceMatcher(
            None, entry, word_to_match
        ).get_opcodes():
            match code:
                case "equal":
                    markup += f"<span foreground='#00703C'>{word_to_match[wtm_start:wtm_stop]}</span>"
                case "replace" | "insert":
                    markup += word_to_match[wtm_start:wtm_stop]
        return Label(markup=markup)

    def find_and_tweak_matches(self, entry):
        matches = []

        for match in process.extract(
            query=entry,
            choices=self.app_list,
            scorer=lambda entry, match: fuzz.WRatio(entry, match)
            + (
                69 if match.startswith(entry) else 0
            ),  # priotize match if it starts with specific letter
        ):
            if match[1]:  # if score is not 0
                matches.append(match[0])
        return matches

    def populate_matchbox(self, entry_text):
        utils.destroy_useless_children(self.matchbox, 0)
        if not entry_text:
            return

        for match in self.find_and_tweak_matches(entry_text):
            self.matchbox.add(
                Button(
                    child=self.create_and_style_label(entry_text, match),
                    on_clicked=lambda *args, value=match: self.run_the_match(value),
                )
            )

    def run_the_match(self, thingy_to_run=None):
        try:
            Hyprland.send_command(
                f"dispatch exec {thingy_to_run if thingy_to_run else self.matchbox.get_children()[0].get_child().get_text()}"
            )
        except IndexError:  # entry empty, so matchbox empty
            return
        self.clear_entry_and_hide()

    def clear_entry_and_hide(self):
        self.entry.delete_text(0, -1)
        utils.destroy_useless_children(self.matchbox, 0)
        self.hide()


app_launcher = AppLauncherPopUp()

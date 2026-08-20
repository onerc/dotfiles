from imports import *
from hacky_widgets import SlidingWaylandWindow


class AppLauncherPopUp(SlidingWaylandWindow):
    def __init__(self):
        self.app_list = sorted(
            {
                PurePath(f"{app.executable}").name  # strip paths
                for app in get_desktop_applications()
            },
            key=str.lower,
        )

        self.matchbox = Box(orientation="v", name="app-launcher-box")
        self.entry = Entry(
            notify_text=lambda entry, *args: self.find_and_tweak_matches(
                entry.get_text()
            ),
            on_activate=lambda *args: self.run_the_match(self.best_match),
            name="app-launcher-entry",
        )

        super().__init__(
            anchor="top center",
            child=Box(orientation="v", children=[self.entry, self.matchbox]),
            monitor=config.hardware.favorite_monitor_index,
            name="app-launcher-window",
            revealer_transition_type="slide-down",
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
        utils.destroy_useless_children(self.matchbox, 0)
        if not entry.strip():  # prevent whitespaces
            self.best_match = None
            return

        self.entry.set_text(entry.lower())

        matches = sorted(
            process.extract(query=entry, choices=self.app_list),
            key=lambda match: match[1],
            reverse=True,
        )

        self.best_match = matches[0][0]

        # populate matchbox
        for match in matches:
            if match[1]:  # if score is not 0
                self.matchbox.add(
                    Button(
                        child=self.create_and_style_label(
                            entry=entry.lower(), word_to_match=match[0]
                        ),
                        on_clicked=lambda *args, value=match[0]: self.run_the_match(
                            thingy_to_run=value
                        ),
                    )
                )

    def run_the_match(self, thingy_to_run):
        if thingy_to_run:
            Hyprland.send_command(f'dispatch hl.dsp.exec_cmd("{thingy_to_run}")')
            self.unslide()

    def slide(self):
        super().slide()
        self.set_keyboard_mode("exclusive")
        self.entry.grab_focus()

    def unslide(self):
        super().unslide()
        self.set_keyboard_mode("none")
        self.entry.delete_text(0, -1)


app_launcher = AppLauncherPopUp()

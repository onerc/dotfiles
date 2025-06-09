from imports import *
from fabricators import now_playing_fabricator


class NowPlaying(Button):
    def __init__(self):
        self.notes = ("♪", "♫", "♬")
        self.now_playing_label = Label(
            label=choice(self.notes), style_classes=["now-playing-label", "passive"]
        )
        # these returns as labels for some reason
        self.bad_labels = ("Music", "Jellyfin")

        super().__init__(
            style_classes="cool-button",
            on_scroll_event=self.on_scroll,
            on_button_release_event=self.on_button_press,  # needed to differentiate button presses
            child=self.now_playing_label,
        )
        now_playing_fabricator.connect(
            "changed", lambda *args: self.update_label(*args)
        )
        self.add_events("scroll")

    def update_label(self, fabricator, value):
        status, *other_info = value.split(r"\n")
        self.now_playing_label.set_label(self.label_handler(other_info))
        toggle_style_class(self, status != "Playing", "passive")

    def label_handler(self, value):
        try:
            album, artist, position, title, volume, player_name = value
            if title in self.bad_labels:
                raise ValueError
            return (
                f"{artist} - {title}"
                if album  # if it's Jellyfin
                else f"{artist.replace(' - Topic', '')} - {title}"
                if artist.endswith(
                    " - Topic"
                )  # if it's YouTube and artist/channel name has "topic"
                else title
            )
        except ValueError:
            return choice(self.notes)

    @staticmethod
    def on_scroll(widget, event):
        match event.direction:
            case 0:
                exec_shell_command_async("playerctl next")
            case 1:
                exec_shell_command_async("playerctl previous")

    @staticmethod
    def on_button_press(widget, event):
        match event.button:
            case 1:
                exec_shell_command_async("playerctl play-pause")
            case 2:
                exec_shell_command_async("playerctl stop")

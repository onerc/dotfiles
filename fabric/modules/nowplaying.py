from imports import *
from fabricators import now_playing_fabricator


class NowPlaying(Button):
    def __init__(self):
        self.now_playing_label = Label(
            label="Nothing is playing", style_classes="passive_nowplaying_label"
        )

        super().__init__(
            style_classes="cool-button",
            on_scroll_event=self.on_scroll,
            on_button_release_event=self.on_button_press,
            child=self.now_playing_label,
        )
        now_playing_fabricator.connect(
            "changed", lambda *args: self.update_label(*args)
        )
        self.add_events("scroll")

    def update_label(self, fabricator, value):
        self.now_playing_label.set_label(self.label_handler(value))
        try:
            if value.split(r"\n")[-5] == "Playing":
                self.now_playing_label.remove_style_class("passive_nowplaying_label")
            else:
                raise IndexError
        except IndexError:
            self.now_playing_label.set_style_classes("passive_nowplaying_label")

    @staticmethod
    def label_handler(value):
        try:
            album, artist, status, position, title, volume, player_name = value.split(
                r"\n"
            )
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
            return "Nothing is playing"

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

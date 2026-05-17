from imports import *
from fabricators import now_playing_fabricator

require_version("Playerctl", "2.0")


class NowPlaying(Button):
    def __init__(self):
        self.manager = Playerctl.PlayerManager()
        self.manager.connect("name-appeared", self.init_player)

        self.notes = ("♪", "♫", "♬")
        # jellyfin returns these as labels for some reason
        self.bad_labels = ("Music", "Jellyfin", "Search", gethostname())

        self.now_playing_label = Label(
            label=choice(self.notes), style_classes=["now-playing-label", "passive"]
        )

        super().__init__(
            style_classes="cool-button",
            on_scroll_event=self.on_scroll,
            on_button_release_event=self.on_button_press,  # needed to differentiate button presses
            child=self.now_playing_label,
        )

        self.add_events("scroll")

    def init_player(self, manager, name):
        self.player = Playerctl.Player.new_from_name(name)
        self.player.connect("playback-status", self.on_play, self.manager)
        self.player.connect("metadata", self.on_metadata, self.manager)
        self.manager.manage_player(self.player)

    def on_play(self, player, playback_status, manager):
        match playback_status:
            case 0 | 1:
                utils.toggle_style_class(self, playback_status, "passive")
            case 2:
                self.rewind()

    @utils.suppress_exceptions(ValueError)
    def on_metadata(self, player, metadata, manager):

        track_id, title, album, artist, url, length = dict(metadata).values()
        artist = "".join(artist)

        if not title or title in self.bad_labels:
            self.rewind()
            return

        self.now_playing_label.remove_style_class("passive")

        self.now_playing_label.set_label(
            f"{artist} - {title}"
            if album  # if it's Jellyfin
            else f"{artist.replace(' - Topic', '')} - {title}"
            if artist.endswith(
                " - Topic"
            )  # if it's YouTube and artist/channel name has "topic"
            else title
        )

    def rewind(self):
        self.now_playing_label.set_label(choice(self.notes))
        self.now_playing_label.add_style_class("passive")

    @utils.suppress_exceptions((AttributeError, GLib.GError))
    def on_scroll(self, widget, event):
        match event.direction:
            case 0:
                self.player.next()
            case 1:
                self.player.previous()

    @utils.suppress_exceptions(AttributeError)
    def on_button_press(self, widget, event):
        match event.button:
            case 1:
                self.player.play_pause()
            case 2:
                self.player.stop()


class OldNowPlaying(Button):
    def __init__(self):

        self.notes = ("♪", "♫", "♬")

        self.now_playing_label = Label(
            label=choice(self.notes), style_classes=["now-playing-label", "passive"]
        )
        # jellyfin returns these as labels for some reason
        self.bad_labels = ("Music", "Jellyfin", "Search", gethostname())

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
        utils.toggle_style_class(self, status != "Playing", "passive")
        self.now_playing_label.set_label(self.label_handler(other_info))

    def label_handler(self, value):
        try:
            album, artist, title, volume, player_name = value
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

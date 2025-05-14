from imports import *


class SpeakerVolume(Button):
    def __init__(self):
        self.audio = Audio(on_speaker_changed=self.label_and_icon_handler)

        self.icon_stack = Stack(
            transition_type="slide-up-down",
            transition_duration=Config.transition_duration,
        )
        for audio_level in ["overamplified", "high", "medium", "low", "muted"]:
            self.icon_stack.add_named(
                Image(
                    icon_name=f"audio-volume-{audio_level}-symbolic",
                    icon_size=Config.icon_size,
                    name="icon",
                ),
                name=audio_level,
            )

        self.label_stack = Stack(
            transition_type="slide-up-down",
            transition_duration=Config.transition_duration,
        )
        for volume_step in range(100, -10, -Config.speaker_volume_increment):
            self.label_stack.add_named(
                Label(label=f"%{volume_step}", style_classes="revealer-label"),
                name=f"{volume_step}",
            )

        self.label_stack.add_named(
            Label(label="N/A", style_classes="revealer-label"), name="N/A"
        )

        self.revealer = Revealer(
            child=self.label_stack,
            transition_type="slide-left",
            transition_duration=Config.transition_duration,
        )

        super().__init__(
            style_classes="cool-button",
            on_clicked=self.mute_handler,
            on_scroll_event=self.scroll_handler,
            on_enter_notify_event=lambda *args: self.revealer.set_reveal_child(True),
            on_leave_notify_event=lambda *args: self.revealer.set_reveal_child(False),
            child=Box(
                children=[
                    self.icon_stack,
                    self.revealer,
                ]
            ),
        )
        self.add_events("scroll")

    def scroll_handler(self, widget, event):
        if self.audio.speaker.name != Config.unwanted_sink:
            match not event.direction:
                case 0:
                    self.audio.speaker.volume -= Config.speaker_volume_increment
                case 1:
                    self.audio.speaker.volume += Config.speaker_volume_increment

    def mute_handler(self, *args):
        self.audio.speaker.muted = not self.audio.speaker.muted

    def label_and_icon_handler(self, *args):
        match self.audio.speaker.name:
            case Config.unwanted_sink:
                label = "N/A"
                icon = "muted"
            case _:
                label = f"{round(self.audio.speaker.volume)}"
                icon = self.icon_name_handler()

        self.label_stack.set_visible_child_name(label)
        self.icon_stack.set_visible_child_name(icon)
        self.style_class_handler()

    def icon_name_handler(self):
        if self.audio.speaker.muted:
            return "muted"
        return (
            "overamplified"
            if (volume := self.audio.speaker.volume) > 99
            else "high"
            if volume >= 66
            else "medium"
            if volume >= 33
            else "low"
            if volume >= 1
            else "muted"
        )

    def style_class_handler(self):
        for child in self.label_stack:
            toggle_style_class(child, self.audio.speaker.muted, "passive")


class MicVolume(Button):
    def __init__(self):
        self.audio = Audio(on_microphone_changed=self.label_and_icon_handler)

        self.icon_stack = Stack(
            transition_type="slide-up-down",
            transition_duration=Config.transition_duration,
        )
        for volume_level in ["high", "medium", "low", "muted"]:
            self.icon_stack.add_named(
                Image(
                    icon_name=f"microphone-sensitivity-{volume_level}-symbolic",
                    icon_size=Config.icon_size,
                    name="icon",
                ),
                name=volume_level,
            )

        self.label_stack = Stack(
            transition_type="slide-up-down",
            transition_duration=Config.transition_duration,
        )
        for volume_step in range(100, -10, -Config.microphone_volume_increment):
            self.label_stack.add_named(
                Label(label=f"%{volume_step}", style_classes="revealer-label"),
                name=f"{volume_step}",
            )
        self.label_stack.add_named(
            Label(label="N/A", style_classes="revealer-label"), name="N/A"
        )

        self.revealer = Revealer(
            child=self.label_stack,
            transition_type="slide-left",
            transition_duration=Config.transition_duration,
        )

        super().__init__(
            style_classes="cool-button",
            on_clicked=self.mute_handler,
            on_scroll_event=self.scroll_handler,
            on_enter_notify_event=lambda *args: self.revealer.set_reveal_child(True),
            on_leave_notify_event=lambda *args: self.revealer.set_reveal_child(False),
            child=Box(
                children=[
                    self.icon_stack,
                    self.revealer,
                ]
            ),
        )
        self.add_events("scroll")

    def scroll_handler(self, widget, event):
        if self.audio.microphone:
            match event.direction:
                case 1:
                    self.audio.microphone.volume -= Config.microphone_volume_increment
                case 0:
                    self.audio.microphone.volume += Config.microphone_volume_increment
        else:
            self.mic_not_found()

    def mute_handler(self, *args):
        if self.audio.microphone:
            self.audio.microphone.muted = not self.audio.microphone.muted
        else:
            self.mic_not_found()

    def label_and_icon_handler(self, *args):
        self.label_stack.set_visible_child_name(
            f"{round(self.audio.microphone.volume)}"
        )
        self.icon_stack.set_visible_child_name(self.icon_name_handler())
        self.style_class_handler()

    def icon_name_handler(self):
        if self.audio.microphone.muted:
            return "muted"
        return (
            "high"
            if (volume := self.audio.microphone.volume) >= 66
            else "medium"
            if volume >= 33
            else "low"
            if volume >= 1
            else "muted"
        )

    def mic_not_found(self):
        self.label_stack.set_visible_child_name("N/A")
        self.icon_stack.set_visible_child_name("muted")

    def style_class_handler(self):
        for child in self.label_stack:
            toggle_style_class(child, self.audio.microphone.muted, "passive")


class AudioOutputSwitch(Button):
    def __init__(self):
        self.audio = Audio(on_speaker_changed=self.icon_handler)

        self.stack = Stack(
            transition_type="slide-up-down",
            transition_duration=Config.transition_duration,
        )
        for icon in ["video-display", "audio-headphones", "dialog-error"]:
            self.stack.add_named(
                Image(
                    icon_name=f"{icon}-symbolic",
                    icon_size=Config.icon_size,
                    name="icon",
                ),
                name=icon,
            )

        super().__init__(
            style_classes="cool-button",
            on_clicked=self.switch_output,
            child=self.stack,
        )

    def icon_handler(self, *args):
        icon_dict = {
            Config.headphones_name: Config.headphone_icon,
            Config.speaker_name: Config.speaker_icon,
            Config.unwanted_sink: Config.unwanted_sink_icon,
        }
        self.stack.set_visible_child_name(icon_dict[self.audio.speaker.name])

    def switch_output(self, *args):
        for speaker in self.audio.speakers:
            if speaker != self.audio.speaker:
                exec_shell_command_async(f"pactl set-default-sink {speaker.name}")

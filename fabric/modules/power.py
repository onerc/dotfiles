from imports import *


class Power(Button):
    def __init__(self):
        self.current_action = "shutdown"
        self.is_locked = True

        self.icon_stack = Stack(
            transition_type="slide-up-down",
            transition_duration=Config.transition_duration,
        )

        for action in ["shutdown", "reboot"]:
            self.icon_stack.add_named(
                Image(
                    icon_name=f"system-{action}-symbolic",
                    icon_size=Config.icon_size,
                    name="icon",
                    style_classes="passive-power-icon",
                ),
                name=action,
            )

        super().__init__(
            style_classes="cool-button",
            on_button_press_event=lambda *args: self.lock_handler(
                *args, is_pressed=True
            ),
            on_button_release_event=lambda *args: self.lock_handler(
                *args, is_pressed=False
            ),
            on_clicked=lambda *args: self.on_clicked(),
            on_scroll_event=self.on_scroll,
            child=self.icon_stack,
        )
        self.add_events("scroll")

    def on_clicked(self):
        if not self.is_locked:
            exec_shell_command_async(f"{self.current_action} now")

    def on_scroll(self, widget, event):
        self.current_action = "shutdown" if not event.direction else "reboot"
        self.icon_stack.set_visible_child_name(self.current_action)

    def lock_handler(self, widget, event, is_pressed):
        if event.button == 3:
            self.is_locked = not is_pressed
            for child in self.icon_stack.get_children():
                (child.remove_style_class if is_pressed else child.add_style_class)(
                    "passive-power-icon"
                )

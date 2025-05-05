from imports import *


class Power(Button):
    def __init__(self):
        self.is_shutdown = True
        self.is_locked = True
        self.is_clicked_once = False

        self.icon_stack = Stack(
            transition_type="slide-up-down",
            transition_duration=Config.transition_duration,
        )
        self.label_stack = Stack(
            transition_type="slide-up-down",
            transition_duration=Config.transition_duration,
        )

        for action in ["Shutdown", "Reboot"]:
            self.icon_stack.add_named(
                Image(
                    icon_name=f"system-{action.lower()}-symbolic",
                    icon_size=Config.icon_size,
                    name="icon",
                ),
                name=action,
            )
            self.label_stack.add_named(
                Label(label=action, style_classes="passive_power_label"), name=action
            )

        self.revealer = Revealer(
            transition_type="slide-left",
            transition_duration=Config.transition_duration,
            child=self.label_stack,
        )
        super().__init__(
            style_classes="cool-button",
            on_enter_notify_event=lambda *args: self.revealer.set_reveal_child(True),
            on_leave_notify_event=lambda *args: self.on_leave(),
            on_clicked=lambda *args: self.on_clicked(),
            on_scroll_event=self.on_scroll,
            child=Box(
                children=[
                    self.icon_stack,
                    self.revealer,
                ]
            ),
        )
        self.add_events("scroll")

    def on_leave(self):
        self.revealer.set_reveal_child(False)
        self.is_clicked_once = 0
        self.style_handler()

    def on_clicked(self):
        if self.is_clicked_once:
            exec_shell_command_async("alacritty" if self.is_shutdown else "engrampa")
            self.is_clicked_once = False
        else:
            self.is_clicked_once = True

        self.style_handler()

    def style_handler(self):
        for child in self.label_stack.get_children():
            child.set_style_classes(
                "active_power_label" if self.is_clicked_once else "passive_power_label"
            )

    def on_scroll(self, widget, event):
        self.is_shutdown = not event.direction
        if self.is_shutdown:
            self.icon_stack.set_visible_child_name("Shutdown")
            self.label_stack.set_visible_child_name("Shutdown")
        else:
            self.icon_stack.set_visible_child_name("Reboot")
            self.label_stack.set_visible_child_name("Reboot")



from imports import *


class SlidingWaylandWindow(WaylandWindow):
    def __init__(
        self,
        child: Box,
        revealer_transition_type: str,
        **kwargs,
    ):

        self.revealer = Revealer(
            transition_duration=config.eye_candy.transition_duration,
            transition_type=revealer_transition_type,
            child=child,
        )
        super().__init__(
            child=Box(style="min-height: 1px", children=self.revealer),
            **kwargs,
        )

    def slide(self):
        self.show()
        self.revealer.set_reveal_child(True)

    def unslide(self):
        self.revealer.set_reveal_child(False)

        GLib.timeout_add(
            config.eye_candy.transition_duration,
            lambda: (
                self.hide(),
                False,
            )[-1],
        )

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

        self.revealer.connect(
            "notify::child-revealed",
            lambda *args: (
                self.hide() if not self.revealer.get_child_revealed() else None
            ),
        )

    def slide(self):
        self.show()
        self.revealer.set_reveal_child(True)

    def unslide(self):
        self.revealer.set_reveal_child(False)

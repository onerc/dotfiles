from imports import *

from modules.hardware_info import HardwareInfo
from modules.calendar import theCalendar


class PopUp(WaylandWindow):
    def __init__(self):
        self.stack = Stack(
            transition_duration=Config.transition_duration,
            transition_type="slide-left-right",
        )
        self.stack.add_titled(theCalendar(), name="calendar", title="Calendar")
        self.stack.add_titled(HardwareInfo(), name="stats", title="Stats")
        self.stack_switcher = Gtk.StackSwitcher(visible=True)
        self.stack_switcher.set_stack(self.stack)

        for button in self.stack_switcher.get_children():
            button.set_hexpand(True)
            button.set_name("stack-switcher")
        super().__init__(
            title="big-popup",
            anchor="top center",
            visible=False,
            child=Box(orientation="v", children=[self.stack_switcher, self.stack]),
        )


pop_up = PopUp()

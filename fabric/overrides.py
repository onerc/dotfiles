from imports import *
from modules.calendar import calendar


class OverriddenDateTime(DateTime):
    def __init__(self):
        super().__init__(formatters="%H:%M", style_classes="cool-button")

    def do_handle_press(self, _, event, *args):
        if event.button == 1:
            toggle_visibility(calendar)


# removing this and just styling the button causes them to get styled late when the bar is started
class OverriddenWorkspaceButton(WorkspaceButton):
    def do_bake_label(self):
        self.children = Label(self._label.format(button=self))


class OverriddenWorkspaces(HyprlandWorkspaces):
    def __init__(self):
        super().__init__(
            buttons=[
                OverriddenWorkspaceButton(
                    id=workspace_id,
                    label=f"{workspace_id}",
                    style_classes=["workspace-button", "cool-button"],
                )
                for workspace_id in range(1, Config.number_of_workspaces + 1)
            ]
        )

    def scroll_handler(self, _, event):
        pass

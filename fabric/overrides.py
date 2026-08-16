from imports import *
from modules.calendar import calendar


class OverriddenDateTime(DateTime):
    def __init__(self):
        super().__init__(formatters="%H:%M", style_classes="cool-button")

    def do_handle_press(self, _, event, *args):
        if event.button == 1:
            utils.cooler_toggle_visibility(calendar)


class OverriddenWorkspaces(HyprlandWorkspaces):
    def __init__(self):
        super().__init__(
            buttons=[
                WorkspaceButton(
                    id=workspace_id,
                    label=f"{workspace_id}",
                    style_classes=["workspace-button", "cool-button"],
                    style="padding:0 0.45rem",  # temporary solution, hopefully
                )
                for workspace_id in range(
                    1, config.window_manager.number_of_workspaces + 1
                )
            ]
        )

    def do_handle_scroll(self, _, event):
        pass

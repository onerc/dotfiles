from imports import *


class OverriddenWorkspaceButton(WorkspaceButton):
    def do_bake_label(self):
        self.children = Label(self._label.format(button=self))


class OverriddenWorkspaces(Workspaces):
    def __init__(self):
        super().__init__(
            buttons=[
                OverriddenWorkspaceButton(
                    id=workspace_id,
                    label=f"{workspace_id}",
                    style_classes=["workspacebutton", "cool-button"],
                )
                for workspace_id in range(1, 11)
            ]
        )

    def scroll_handler(self, _, event):
        pass

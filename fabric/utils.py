from imports import *


def toggle_style_class(parent: Gtk.Widget, condition: bool, class_name: str) -> None:
    for child in parent.get_children():
        (child.add_style_class if condition else child.remove_style_class)(class_name)


def toggle_visibility(window: WaylandWindow):
    window.hide() if window.get_visible() else window.show()

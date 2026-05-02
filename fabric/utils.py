from imports import *


def toggle_style_class(
    parent: Gtk.Widget, condition: bool | int, class_name: str
) -> None:
    for child in parent.get_children():
        (child.add_style_class if condition else child.remove_style_class)(class_name)


def toggle_visibility(window: WaylandWindow) -> None:
    (window.hide if window.get_visible() else window.show)()


def destroy_useless_children(parent: Box, children_start_index: int) -> None:
    for child in parent.get_children()[children_start_index:]:
        child.destroy()


def suppress_exceptions(exception_to_suppress):
    def inner(f):
        def wrapper(*args, **kwargs):
            try:
                f(*args, **kwargs)
            except exception_to_suppress:
                pass

        return wrapper
    return inner

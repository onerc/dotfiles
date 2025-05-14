from imports import *


def toggle_style_class(child_to_style: Gtk.Widget, condition: bool, class_name: str):
    (
        child_to_style.add_style_class
        if condition
        else child_to_style.remove_style_class
    )(class_name)

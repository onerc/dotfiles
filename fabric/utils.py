from modules.popup import pop_up
from modules.applauncher import app_launcher


def window_focus(action):
    match action:
        case "show":
            pop_up.set_keyboard_mode("exclusive")
            app_launcher.entry.grab_focus()
            pop_up.show()
        case "hide":
            pop_up.set_keyboard_mode("on-demand")
            app_launcher.entry.grab_remove()
            pop_up.hide()

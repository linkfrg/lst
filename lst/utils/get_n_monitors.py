from gi.repository import Gdk

def get_n_monitors() -> list:
    return range(Gdk.Display.get_default().get_n_monitors())
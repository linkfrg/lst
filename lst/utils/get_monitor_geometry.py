import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk
from typing import Tuple
def get_monitor_geometry(monitor_id: int = None) -> Tuple[int]:
    display = Gdk.Display.get_default()
    if monitor_id:
        monitor = display.get_monitor(monitor_id)
    else:
        x = display.get_pointer()[1]
        y = display.get_pointer()[2]
        monitor = display.get_monitor_at_point(x, y)
    geometry = monitor.get_geometry()
    return geometry.width, geometry.height


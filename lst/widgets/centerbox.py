from gi.repository import Gtk
from lst.base_widget import BaseWidget, GObject
from typing import Any

ORIENTATION = {
    "h": Gtk.Orientation.HORIZONTAL,
    "v": Gtk.Orientation.VERTICAL,
}


class CenterBox(Gtk.Box, BaseWidget):
    """
    Bases: `Gtk.Box <https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Box.html>`_, :class:`~lst.base_widget.BaseWidget`.

    A box widget that contain three widgets, which will be placed at the start, center and of the end of the container.

    Parameters:
        start_widget(``Gtk.Widget``): Widget that will be placed at start of the container.
        center_widget(``Gtk.Widget``): Widget that will be placed at center of the container.
        end_widget(``Gtk.Widget``): Widget that will be placed at end of the container.
        orientation(``str``, optional): Orientation of the widget. Possible values: ``"h"``, ``"v"``.

    .. code-block:: python
    
        Widget.CenterBox(
            start_widget=Widget.Label('start'),
            center_widget=Widget.Label('center'),
            end_widget=Widget.Label('end'),
            orientation='h'
        )
    """

    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(
        self,
        start_widget: Gtk.Widget,
        center_widget: Gtk.Widget,
        end_widget: Gtk.Widget,
        orientation: str = "h",
        **kwargs,
    ):
        Gtk.Box.__init__(self)
        BaseWidget.__init__(self, **kwargs)

        self._start_widget = None
        self._center_widget = None
        self._end_widget = None

        self.start_widget = start_widget
        self.center_widget = center_widget
        self.end_widget = end_widget
        self.orientation = orientation

    @GObject.Property
    def start_widget(self) -> Gtk.Widget:
        return self._start_widget

    @start_widget.setter
    def start_widget(self, widget: Gtk.Widget) -> None:
        if self.start_widget:
            self.remove(self.get_children()[0])

        self.pack_start(widget, True, True, 0)
        self._start_widget = widget

    @GObject.Property
    def center_widget(self) -> Gtk.Widget:
        return self._center_widget

    @center_widget.setter
    def center_widget(self, widget: Gtk.Widget) -> None:
        if self.center_widget:
            self.remove(self.get_children()[1])

        super().set_center_widget(widget)
        self._center_widget = widget

    @GObject.Property
    def end_widget(self) -> Gtk.Widget:
        return self._end_widget

    @end_widget.setter
    def end_widget(self, widget: Gtk.Widget) -> None:
        if self.end_widget:
            self.remove(self.get_children()[2])

        self.pack_end(widget, True, True, 0)
        self._end_widget = widget

    def set_property(self, property_name: str, value: Any) -> None:
        if property_name == "orientation":
            super().set_property("orientation", ORIENTATION[value])
        else:
            super().set_property(property_name, value)

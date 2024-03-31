from gi.repository import Gtk
from lst.widgets.widget import Widget, GObject

ORIENTATION = {
    "h": Gtk.Orientation.HORIZONTAL,
    "v": Gtk.Orientation.VERTICAL,
}


class CenterBox(Gtk.Box, Widget):
    __gproperties__ = {**Widget.gproperties}

    def __init__(
        self,
        start_widget: Gtk.Widget,
        center_widget: Gtk.Widget,
        end_widget: Gtk.Widget,
        orientation: str = "h",
        spacing: int = 0,
        **kwargs
    ):
        Gtk.Box.__init__(
            self, orientation=ORIENTATION[orientation], spacing=spacing
        )
        Widget.__init__(self, **kwargs)

        self._start_widget = None
        self._center_widget = None
        self._end_widget = None

        self.start_widget = start_widget
        self.center_widget = center_widget
        self.end_widget = end_widget

    @GObject.Property
    def start_widget(self) -> Gtk.Widget:
        return self._start_widget

    @start_widget.setter
    def start_widget(self, widget: Gtk.Widget) -> None:
        if self.start_widget:
            self.remove(self.get_children()[0])

        self.pack_start(widget, True, True, 0)
        self._start_widget = widget

    def set_start_widget(self, widget: Gtk.Widget) -> None:
        self.start_widget = widget

    @GObject.Property
    def center_widget(self) -> Gtk.Widget:
        return self._center_widget

    @center_widget.setter
    def center_widget(self, widget: Gtk.Widget) -> None:
        if self.center_widget:
            self.remove(self.get_children()[1])

        super().set_center_widget(widget)
        self._center_widget = widget

    def set_center_widget(self, widget: Gtk.Widget) -> None:
        self.center_widget = widget

    @GObject.Property
    def end_widget(self) -> Gtk.Widget:
        return self._end_widget

    @end_widget.setter
    def end_widget(self, widget: Gtk.Widget) -> None:
        if self.end_widget:
            self.remove(self.get_children()[2])
            
        self.pack_end(widget, True, True, 0)
        self._end_widget = widget

    def set_end_widget(self, widget: Gtk.Widget) -> None:
        self.end_widget = widget

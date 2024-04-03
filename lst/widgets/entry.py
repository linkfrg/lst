from gi.repository import Gtk, GObject
from lst.widgets.widget import Widget


class Entry(Gtk.Entry, Widget):
    __gproperties__ = {**Widget.gproperties}

    def __init__(
        self,
        placeholder: str = None,
        on_accept: callable = None,
        on_change: callable = None,
        **kwargs
    ):
        Gtk.Entry.__init__(self)
        Widget.__init__(self, **kwargs)

        self._on_accept = None
        self._on_change = None

        self.set_on_accept(on_accept)
        self.set_on_change(on_change)

        if placeholder:
            self.set_placeholder_text(placeholder)

        if on_accept:
            self.connect("activate", lambda x: on_accept(x))

        if on_change:
            self.connect("notify::text", lambda x, y: on_change(x))

    @GObject.Property
    def on_accept(self) -> callable:
        return self._on_accept

    @on_accept.setter
    def on_accept(self, value: callable) -> None:
        self._on_accept = value

    def set_on_accept(self, value: callable) -> None:
        self.on_accept = value

    @GObject.Property
    def on_change(self) -> callable:
        return self._on_change

    @on_change.setter
    def on_change(self, value: callable) -> None:
        self._on_change = value

    def set_on_change(self, value: callable) -> None:
        self.on_change = value

from gi.repository import Gtk, GObject
from lst.base_widget import BaseWidget


class Entry(Gtk.Entry, BaseWidget):
    """
    Bases: `Gtk.Entry <https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Entry.html>`_, :class:`~lst.base_widget.BaseWidget`.

    An input field. To make it work set ``kb_mode`` of window to ``"on_demand"`` or ``"exclusive"``.

    Parameters:
        on_accept(``callable``, optional): The function that will be called when user hits the Enter key.
        on_change(``callable``, optional): The function that will be called when text of the widget is changed(e.g user wrote something into entry).

    .. code-block:: python
    
        Widget.Entry(
            on_accept=lambda self: print(self),
            on_change=lambda self: print(self),
        )
    """
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(
        self,
        on_accept: callable = None,
        on_change: callable = None,
        **kwargs
    ):
        Gtk.Entry.__init__(self)
        BaseWidget.__init__(self, **kwargs)

        self._on_accept = None
        self._on_change = None

        self.on_accept = on_accept
        self.on_change = on_change

        self.connect("activate", lambda x: on_accept(x) if self.on_accept else None)

        self.connect("notify::text", lambda x, y: on_change(x) if self.on_change else None)

    @GObject.Property
    def on_accept(self) -> callable:
        return self._on_accept

    @on_accept.setter
    def on_accept(self, value: callable) -> None:
        self._on_accept = value

    @GObject.Property
    def on_change(self) -> callable:
        return self._on_change

    @on_change.setter
    def on_change(self, value: callable) -> None:
        self._on_change = value

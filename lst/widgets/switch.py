from gi.repository import Gtk, GObject
from lst.base_widget import BaseWidget


class Switch(Gtk.Switch, BaseWidget):
    """
    Bases: `Gtk.Switch <https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Switch.html>`_, :class:`~lst.base_widget.BaseWidget`.
    
    A switch.

    Parameters:
        on_activate(``callable``, optional): Function to call on activate.
        on_deactivate(``callable``, optional): Function to call on deactivate.
    
    .. code-block:: python
    
        Widget.Switch(
            state=True,
            on_activate=lambda self: print(self),
            on_deactivate=lambda self: print(self)
        )
    """
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(
        self,
        on_activate: callable = None,
        on_deactivate: callable = None,
        **kwargs,
    ):
        Gtk.Switch.__init__(self)
        BaseWidget.__init__(self, **kwargs)
        self._on_activate = None
        self._on_deactivate = None
        self.on_activate = on_activate
        self.on_deactivate = on_deactivate

        self.connect("state-set", lambda *args: self.__callback())

    def __callback(self) -> None:
        if self.state:
            if self._on_deactivate:
                self._on_deactivate(self)
        else:
            if self._on_activate:
                self._on_activate(self)

    @GObject.Property
    def on_activate(self) -> callable:
        return self._on_activate

    @on_activate.setter
    def on_activate(self, value: callable) -> None:
        self._on_activate = value

    @GObject.Property
    def on_deactivate(self) -> callable:
        return self._on_deactivate

    @on_deactivate.setter
    def on_deactivate(self, value: callable) -> None:
        self._on_deactivate = value

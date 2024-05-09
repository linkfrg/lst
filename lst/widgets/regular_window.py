from lst.app import app
from gi.repository import Gtk, GObject
from lst.base_widget import BaseWidget


class RegularWindow(Gtk.Window, BaseWidget):
    """
    Bases: `Gtk.Window <https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Window.html>`_, :class:`~lst.base_widget.BaseWidget`.

    A window that looks like a normal window of any other application.
    
    Parameters:
        namespace(``str``): Name of the window, that will be used to access from CLI and :class:`~lst.app.LstApp`. It must be unique.
        child(``Gtk.Widget``, optional): Child widget.
        show_header_bar(``bool``, optional): Whether header bar is shown.
        show_close_button(``bool``, optional): Whether close button is shown. Work only if ``header_bar`` set to ``True``.

    .. code-block:: python

        Widget.RegularWindow(
            child=Widget.Label("brrr skibidi dop dop yes yes"),
            show_header_bar=True,
            show_close_button=True,
            title="ЭЩКЕРЕЕЕ",
            namespace='some-regular-window',
        )
    """
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(
        self,
        namespace: str,
        child: Gtk.Widget = None,
        show_header_bar: bool = False,
        show_close_button: bool = False,
        **kwargs,
    ):
        Gtk.Window.__init__(self)
        BaseWidget.__init__(self, **kwargs)

        self._show_header_bar = None
        self._show_close_button = None
        self._header_bar = None

        self.child = child
        self.show_header_bar = show_header_bar
        self.show_close_button = show_close_button

        app.add_window(namespace, self)

    @GObject.Property
    def child(self) -> Gtk.Widget:
        return self._child

    @child.setter
    def child(self, value: Gtk.Widget) -> None:
        current = self.get_children()
        if current != []:
            if not isinstance(current[0], Gtk.HeaderBar):
                self.remove(current[0])
        if value:
            self.add(value)
    
    @GObject.Property
    def show_header_bar(self) -> bool:
        return self._show_header_bar
    
    @show_header_bar.setter
    def show_header_bar(self, value: bool) -> None:
        if value:
            self._header_bar = Gtk.HeaderBar()
            self._header_bar.set_show_close_button(True)
            self._header_bar.set_title(self.title)
            self._header_bar.show()
            self.set_titlebar(self._header_bar)
        else:
            self.set_titlebar(None)

        self._show_header_bar = value
    
    @GObject.Property
    def show_close_button(self) -> bool:
        return self._show_header_bar
    
    @show_close_button.setter
    def show_close_button(self, value: bool) -> None:
        if self._header_bar:
            self._header_bar.set_show_close_button(value)
        self._show_header_bar = value

from lst.app import app
from gi.repository import Gtk, GObject
from lst.widgets.widget import Widget


class RegularWindow(Gtk.Window, Widget):
    __gproperties__ = {**Widget.gproperties}

    def __init__(
        self,
        namespace: str,
        title: str = None,
        show_header_bar: bool = False,
        child: Gtk.Widget = None,
        is_open: bool = True,
        resizable: bool = True,
        width: int = 2,
        height: int = 2,
        **kwargs,
    ):
        Gtk.Window.__init__(self)

        if title:
            if show_header_bar:
                header_bar = Gtk.HeaderBar()
                header_bar.set_show_close_button(True)
                header_bar.set_title(title)
                header_bar.show()
                self.set_titlebar(header_bar)
            else:
                self.set_title(title)

        Widget.__init__(self, **kwargs)

        self._child = None
        self.child = child
        self.is_open = is_open

        self.set_size_request(width, height)
        self.set_resizable(resizable)

        app.add_window(namespace, self)

    @GObject.Property
    def is_open(self) -> bool:
        return self._is_open
    
    @is_open.setter
    def is_open(self, value: bool) -> None:
        self._is_open = value
        if value:
            self.show()
        else:
            self.hide()

    def set_is_open(self, value: bool) -> None:
        self.is_open = value

    @GObject.Property
    def child(self) -> Gtk.Widget:
        return self._child

    @child.setter
    def child(self, value: Gtk.Widget) -> None:
        if value:
            current = self.get_children()
            if current != []:
                if not isinstance(current[0], Gtk.HeaderBar):
                    self.remove(current[0])
            self.add(value)
            self._child = value

    def set_child(self, value: Gtk.Widget) -> None:
        self.child = value

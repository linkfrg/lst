from lst.app import app
from gi.repository import Gtk, GtkLayerShell, GObject, Gdk
from lst.base_widget import BaseWidget
from typing import List

LAYER = {
    "background": GtkLayerShell.Layer.BACKGROUND,
    "bottom": GtkLayerShell.Layer.BOTTOM,
    "top": GtkLayerShell.Layer.TOP,
    "overlay": GtkLayerShell.Layer.OVERLAY,
}

KB_MODE = {
    None: GtkLayerShell.KeyboardMode.NONE,
    "none": GtkLayerShell.KeyboardMode.NONE,
    "exclusive": GtkLayerShell.KeyboardMode.EXCLUSIVE,
    "on_demand": GtkLayerShell.KeyboardMode.ON_DEMAND,
}


ANCHOR = {
    "bottom": GtkLayerShell.Edge.BOTTOM,
    "left": GtkLayerShell.Edge.LEFT,
    "right": GtkLayerShell.Edge.RIGHT,
    "top": GtkLayerShell.Edge.TOP,
}


class Window(Gtk.Window, BaseWidget):
    """
    Bases: `Gtk.Window <https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Window.html>`_, :class:`~lst.base_widget.BaseWidget`.

    The toplevel widget that contain everything.

    Parameters:
        namespace(``str``): Name of the window, that will be used to access from CLI and :class:`~lst.app.LstApp`. It must be unique. It is also name of the layer.
        child(``Gtk.Widget``, optional): Child widget.
        monitor(``int``, optional): Monitor number on which to display the window.
        anchor(``List[str]``, optional): List of anchors.if the list is empty, the window will be located in the middle of the screen. Possible anchor values: ``"bottom"``, ``"left"``, ``"right"``, ``"top"``. 
        exclusive(``bool``, optional): Whether the compositor should reserve space for the window.
        layer(``str``, optional): Layer of the surface. Possible values: ``"background"``, ``"bottom"``, ``"top"``, ``"overlay"``.
        kb_mode(``str``, optional): Whether window should receive keyboard events from the compositor. Possible values: ``"none"``, ``"exclusive"``, `"on_demand"``.
        popup(``bool``, optional): Whether window should close on ESC. Work only if ``kb_mode`` set to ``"exclusive"`` or `"on_demand"``.

    .. code-block:: python

        Widget.Window(
            namespace="example_window",
            child=Widget.Label('heh'),
            monitor=0,
            anchor=["top", "right"],
            exclusive=True,
            layer="top",
            kb_mode="none",
            popup=False
        )    

    """
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(
        self,
        namespace: str,
        child: Gtk.Widget = None,
        monitor: int = None,
        anchor: List[str] = [],
        exclusive: bool = False,
        layer: str = "top",
        kb_mode: str = "none",
        popup: bool = False,
        **kwargs,
    ):
        Gtk.Window.__init__(self)
        GtkLayerShell.init_for_window(self)

        self._child = None
        self._anchor = None
        self._exclusive = None
        self._namespace = None
        self._layer = None
        self._kb_mode = None
        self._popup = None
        self._monitor = None

        self.child = child
        self.anchor = anchor
        self.exclusive = exclusive
        self.namespace = namespace
        self.layer = layer
        self.kb_mode = kb_mode
        self.monitor = monitor
        self.popup = popup

        app.add_window(namespace, self)
        self.connect("key-press-event", lambda x, event: self.__close_popup(event))

        BaseWidget.__init__(self, **kwargs)

    def __close_popup(self, event):
        if self._popup:
            if event.get_keyval()[1] == Gdk.KEY_Escape:
                app.close_window(GtkLayerShell.get_namespace(self))

    @GObject.Property
    def child(self) -> Gtk.Widget:
        return self._child

    @child.setter
    def child(self, value: Gtk.Widget) -> None:
        if value:
            if self.get_children() != []:
                self.remove(self.get_children()[0])
            self.add(value)
            self._child = value

    @GObject.Property
    def anchor(self) -> list:
        return self._anchor

    @anchor.setter
    def anchor(self, value: list) -> None:
        self._anchor = value
        for i in value:
            GtkLayerShell.set_anchor(self, ANCHOR[i], 1)

    @GObject.Property
    def exclusive(self) -> bool:
        return self._exclusive

    @exclusive.setter
    def exclusive(self, value: bool) -> None:
        self._exclusive = value
        if value:
            GtkLayerShell.auto_exclusive_zone_enable(self)
        else:
            GtkLayerShell.set_exclusive_zone(self, 0)

    @GObject.Property
    def namespace(self) -> str:
        return self._namespace

    @namespace.setter
    def namespace(self, value: str) -> None:
        self._namespace = value
        GtkLayerShell.set_namespace(self, name_space=value)

    @GObject.Property
    def layer(self) -> str:
        return self._layer

    @layer.setter
    def layer(self, value: str) -> None:
        self._layer = value
        GtkLayerShell.set_layer(self, LAYER[value])

    @GObject.Property
    def kb_mode(self) -> str:
        return self._kb_mode

    @kb_mode.setter
    def kb_mode(self, value: str) -> None:
        self._kb_mode = value
        GtkLayerShell.set_keyboard_mode(self, KB_MODE[value])

    @GObject.Property
    def popup(self) -> bool:
        return self._popup

    @popup.setter
    def popup(self, value: bool) -> None:
        self._popup = value

    @GObject.Property
    def monitor(self) -> int:
        return self._monitor

    @monitor.setter
    def monitor(self, value: int) -> None:
        if value is None:
            return
        gdkmonitor = Gdk.Display.get_default().get_monitor(value)
        if gdkmonitor is None:
            print(f"No such monitor with id: {value}")
            return
        GtkLayerShell.set_monitor(self, gdkmonitor)
        self._monitor = value

    def toggle(self) -> bool:
        self.visible = not self.visible
        return self.visible
    
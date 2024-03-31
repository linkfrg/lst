from lst.app import app
from gi.repository import Gtk, GtkLayerShell, GObject, Gdk
from lst.widgets.widget import Widget

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

class Window(Gtk.Window, Widget):
    __gproperties__ = {**Widget.gproperties}

    def __init__(
        self,
        namespace: str,
        child: Gtk.Widget = None,
        monitor: int = None,
        anchor: list = [],
        exclusive: bool = False,
        layer: str = "top",
        kb_mode: str = "none",
        popup: bool = False,
        is_open: bool = True,
        width: int = 2,
        height: int = 2,
        **kwargs
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
        self._is_open = None

        self.child = child
        self.anchor = anchor
        self.exclusive = exclusive
        self.namespace = namespace
        self.layer = layer
        self.kb_mode = kb_mode
        self.monitor = monitor
        self.popup = popup

        self.set_size_request(width, height)
        app.add_window(namespace, self)
        self.connect("key-press-event", lambda x, event: self.__close_popup(event))
        
        Widget.__init__(self, **kwargs)
        self.is_open = is_open


    def __close_popup(self, event):
        if self._popup:
            if event.get_keyval()[1] == Gdk.KEY_Escape:
                app.close_window(GtkLayerShell.get_namespace(self))

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
            if self.get_children() != []:
                self.remove(self.get_children()[0])
            self.add(value)
            self._child = value

    def set_child(self, value: Gtk.Widget) -> None:
        self.child = value

    @GObject.Property
    def anchor(self) -> list:
        return self._anchor

    @anchor.setter
    def anchor(self, value: list) -> None:
        self._anchor = value
        for i in value:
            GtkLayerShell.set_anchor(self, ANCHOR[i], 1)

    def set_anchor(self, value: list) -> None:
        self.anchor = value

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

    def set_exclusive(self, value: bool) -> None:
        self.exclusive = value

    @GObject.Property
    def namespace(self) -> str:
        return self._namespace

    @namespace.setter
    def namespace(self, value: str) -> None:
        self._namespace = value
        GtkLayerShell.set_namespace(self, name_space=value)

    def set_namespace(self, value: str) -> None:
        self.namespace = value

    @GObject.Property
    def layer(self) -> str:
        return self._layer

    @layer.setter
    def layer(self, value: str) -> None:
        self._layer = value
        GtkLayerShell.set_layer(self, LAYER[value])

    def set_layer(self, value: str) -> None:
        self.layer = value

    @GObject.Property
    def kb_mode(self) -> str:
        return self._kb_mode

    @kb_mode.setter
    def kb_mode(self, value: str) -> None:
        self._kb_mode = value
        GtkLayerShell.set_keyboard_mode(self, KB_MODE[value])

    def set_kb_mode(self, value: str) -> None:
        self.kb_mode = value

    @GObject.Property
    def popup(self) -> bool:
        return self._popup

    @popup.setter
    def popup(self, value: bool) -> None:
        self._popup = value

    def set_popup(self, value: bool) -> None:
        self.popup = value

    @GObject.Property
    def monitor(self) -> int:
        return self._monitor

    @monitor.setter
    def monitor(self, value: int) -> None:
        if value is None:
            return
        gdkmonitor = Gdk.Display.get_default().get_monitor(value)
        if gdkmonitor is None:
            print(f'No such monitor with id: {value}')
            return
        GtkLayerShell.set_monitor(self, gdkmonitor)
        self._monitor = value

    def set_monitor(self, value: int) -> None:
        self.monitor = value

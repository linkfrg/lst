from gi.repository import Gtk, GObject
from lst.services.base_service import BaseService

ALIGN = {
    "start": Gtk.Align.START,
    "center": Gtk.Align.CENTER,
    "end": Gtk.Align.END,
    "fill": Gtk.Align.FILL,
    "baseline": Gtk.Align.BASELINE,
}


class Widget(Gtk.Widget, BaseService):
    gproperties = __gproperties__ = {}

    def __init__(
        self,
        class_name: str = None,
        valign: str = "fill",
        halign: str = "fill",
        vexpand: bool = False,
        hexpand: bool = False,
        tooltip: str = None,
        style: str = None,
        sensitive: bool = True,
        visible: bool = True,
        connections: list = [],
    ):
        Gtk.Widget.__init__(self)
        BaseService.__init__(self)

        self._class_name = None
        self._style = None
        self._css_provider = None

        self.set_class_name(class_name)
        self.set_valign(valign)
        self.set_halign(halign)
        self.set_vexpand(vexpand)
        self.set_hexpand(hexpand)
        self.set_tooltip_text(tooltip)
        self.set_style(style)
        self.set_sensitive(sensitive)
        self.set_visible(visible)

        for i in connections:
            self.connect_to_gobject(*i)

    @GObject.property
    def class_name(self) -> str:
        return self._class_name

    @class_name.setter
    def class_name(self, value: str) -> None:
        if value:
            style_context = self.get_style_context()
            for c in style_context.list_classes():
                style_context.remove_class(c)

            for name in value.split(" "):
                style_context.add_class(name)

            self._class_name = value

    def set_class_name(self, value: str) -> None:
        self.class_name = value

    def add_class_name(self, value: str) -> None:
        style_context = self.get_style_context()
        style_context.add_class(value)
        self.notify("class-name")

    def remove_class_name(self, value: str) -> None:
        style_context = self.get_style_context()
        style_context.remove_class(value)
        self.notify("class-name")

    @GObject.property
    def style(self) -> str:
        return self._style

    @style.setter
    def style(self, value: str) -> None:
        if value:
            css_provider = Gtk.CssProvider()
            style_formated = "* {" + value + "}"
            css_provider.load_from_data(style_formated.encode())

            self.get_style_context().add_provider(
                css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )
            if self._css_provider:
                self.get_style_context().remove_provider(self._css_provider)
            self._css_provider = css_provider
            self._style = value

    def set_style(self, value: str) -> None:
        self.style = value

    def set_valign(self, value: str) -> None:
        self.set_property("valign", ALIGN[value])

    def set_halign(self, value: str) -> None:
        self.set_property("halign", ALIGN[value])

    def set_vexpand(self, value: bool) -> None:
        self.set_property("vexpand", value)

    def set_hexpand(self, value: bool) -> None:
        self.set_property("hexpand", value)

    def set_tooltip_text(self, value: str) -> None:
        self.set_property("tooltip_text", value)

    def set_sensitive(self, value: bool) -> None:
        self.set_property("sensitive", value)

    def set_visible(self, value: bool) -> None:
        self.set_property("visible", value)
        

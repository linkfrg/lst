from gi.repository import Gtk, GObject
from lst.base_service import Binding
from typing import Any

ALIGN = {
    "start": Gtk.Align.START,
    "center": Gtk.Align.CENTER,
    "end": Gtk.Align.END,
    "fill": Gtk.Align.FILL,
    "baseline": Gtk.Align.BASELINE,
}


class Widget(Gtk.Widget):
    gproperties = __gproperties__ = {}

    def __init__(
        self,
        class_name: str = None,
        valign: str = "fill",
        halign: str = "fill",
        vexpand: bool = False,
        hexpand: bool = False,
        tooltip_text: str = None,
        style: str = None,
        sensitive: bool = True,
        visible: bool = True,
        width_request: int = 2,
        height_request: int = 2,
        **kwargs
    ):
        super().__init__()

        self._class_name = None
        self._style = None
        self._css_provider = None

        self.class_name = class_name
        self.valign = valign
        self.halign = halign
        self.vexpand = vexpand
        self.hexpand = hexpand
        self.tooltip_text = tooltip_text
        self.style = style
        self.sensitive = sensitive
        self.visible = visible
        self.width_request = width_request
        self.height_request = height_request

        for key in kwargs.keys():
            self.set_property(key, kwargs[key])

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

    def set_property(self, property_name: str, value: Any) -> None:
        if value is None:
            return
        if property_name == "valign" or property_name == "halign":
            super().set_property(property_name, ALIGN[value])
        elif isinstance(value, Binding):
            self.bind_property(value.target, value.target_property, property_name, value.transform)
        else:
            super().set_property(property_name, value)

    def __getattribute__(self, name: str) -> Any:
        if name.startswith("set_") and name != "set_property":
            property_name = name.replace('set_', '')
            if self.find_property(property_name):
                return lambda value: self.set_property(property_name, value)
        return super().__getattribute__(name)

    def __setattr__(self, name: str, value: Any) -> None:
        if self.find_property(name):
            self.set_property(name, value)
        else:
            super().__setattr__(name, value)
    
    def __getattr__(self, name: str) -> Any:
        if self.find_property(name):
            return self.get_property(name)
        else:
            super().__getattribute__(name)

    def bind_property(self, target: GObject.Object, target_property: str, source_property: str, transform: callable = None) -> None:
        def callback(*args):
            value = target.get_property(target_property.replace('-', '_'))
            if transform:
                value = transform(value)
            self.set_property(source_property, value)

        target.connect(f"notify::{target_property.replace('_', '-')}", callback)
        callback()

    def bind(self, property_name: str, transform: callable = None) -> Binding:
        return Binding(self, property_name, transform)

    
from gi.repository import GObject, GLib
from typing import Any, Union

class Binding(GObject.Object):
    def __init__(
        self, target: GObject.Object, target_property: str, transform: callable = None
    ):
        self._target = target
        self._target_property = target_property
        self._transform = transform
        super().__init__()

    @GObject.Property
    def target(self) -> GObject.Object:
        return self._target

    @GObject.Property
    def target_property(self) -> str:
        return self._target_property

    @GObject.Property
    def transform(self) -> callable:
        return self._transform


class BaseService(GObject.Object):
    def __init__(self):
        super().__init__()

    def bind(self, property_name: str, transform: callable = None) -> Binding:
        return Binding(self, property_name, transform)

    def emit(self, signal_name: str, *args):
        GLib.idle_add(super().emit, signal_name, *args)

    def notify(self, property_name: str):
        GLib.idle_add(super().notify, property_name)

    def connect_to_gobject(self, gobject: GObject.Object, signal_name: str, callback: callable, *args):
        """
        Connect to signal of another GObject\n
        Gives self as first argument to callback and GObject signal arguments\n
        callback(self, *gobject_args, *args)
        """
        gobject.connect(signal_name, lambda *gobject_args: callback(self, *gobject_args, *args))

    def bind_property(self, target: GObject.Object, target_property: str, source_property: str, transform: callable = None) -> None:
        def callback(*args):
            value = target.get_property(target_property.replace('-', '_'))
            if transform:
                value = transform(value)
            self.set_property(source_property, value)

        target.connect(f"notify::{target_property.replace('_', '-')}", callback)
        callback()

    def set_property(self, property_name: str, value: Any) -> None:
        if value is None:
            return
        if isinstance(value, Binding):
            self.bind_property(value.target, value.target_property, property_name, value.transform)
        else:
            super().set_property(property_name, value)

    def notify_all(self, without: Union[list, str] = None) -> None:
        for i in self.list_properties():
            if without:
                if i.name in without:
                    continue
            self.notify(i.name)

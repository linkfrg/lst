from gi.repository import GObject, GLib
from typing import Union

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

    def notify_all(self, without: Union[list, str] = None) -> None:
        for i in self.list_properties():
            if without:
                if i.name in without:
                    continue
            self.notify(i.name)

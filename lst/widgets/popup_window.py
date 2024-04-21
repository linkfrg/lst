from gi.repository import Gtk
from typing import Any
from lst.widgets.window import Window
from lst.widgets.revealer import Revealer


class PopupWindow(Window):
    def __init__(
        self,
        child: Gtk.Widget = None,
        transition_type: str = "crossfade",
        reveal_child: bool = True,
        **kwargs,
    ):
        self._revealer = Revealer(
            transition_type=transition_type, reveal_child=reveal_child, child=child
        )
        super().__init__(child=self._revealer, **kwargs)
        super().show()

    def set_property(self, property_name: str, value: Any) -> None:
        if property_name == "visible":
            self._revealer.reveal_child = value
        else:
            super().set_property(property_name, value)

    def __getattr__(self, name: str) -> Any:
        if name == 'visible':
            return self._revealer.reveal_child
        else:
            super().__getattribute__(name)

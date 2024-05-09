from gi.repository import Gtk
from typing import Any
from lst.widgets.window import Window
from lst.widgets.revealer import Revealer


class PopupWindow(Window):
    """
    Bases: :class:`~lst.widgets.Widget.Window`
    
    A window that opens and closes with animation.
    
    Parameters:
        child(``Gtk.Widget``, optional): Child widget.
        transition_type(``str``, optional): Type of animation. Possible values: ``"none"``, ``"crossfade"``, ``"slideright"``, ``"slideleft"``, ``"slideup"``, ``"slidedown"``.
        reveal_child(``bool``, optional): Whether the window should reveal the child.
    
    .. code-block:: python
    
        Widget.PopupWindow(
            child=Widget.Label('asdasfajk!!!'),
            transition_type='slidedown',
            reveal_child=True
        )
    """
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
    
    def show(self) -> None:
        self.visible = True
    
    def hide(self) -> None:
        self.visible = False
from gi.repository import Gtk, GObject
from lst.base_widget import BaseWidget
from typing import Any

ORIENTATION = {
    "h": Gtk.Orientation.HORIZONTAL,
    "v": Gtk.Orientation.VERTICAL,
}

VALUE_POS = {
    "left": Gtk.PositionType.LEFT,
    "right": Gtk.PositionType.RIGHT,
    "top": Gtk.PositionType.TOP,
    "bottom": Gtk.PositionType.BOTTOM,
}


class Scale(Gtk.Scale, BaseWidget):
    """
    Bases: `Gtk.Scale <https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Scale.html>`_, :class:`~lst.base_widget.BaseWidget`.
    
    A slider.

    Parameters:
        orientation (``str``, optional): Orientation of the widget. Possible values: ``"h"``, ``"v"``.
        min(``float``, optional): Minimum value.
        max(``float``, optional): Maximum value.
        step(``float``, optional): Step increment.
        value(``float``, optional): Current value.
        on_change(``callable``, optional): Function to call on value change.
        draw_value(``int``, optional): Whether current value is displayed
        value_pos(``str``, optional). Position in which the current value is displayed. Work only if ``draw_value`` set to ``True``.
        Possible values: ``"left"``, `"right"``, `"top"``, `"bottom"``.
    
    .. code-block:: python
        
        Widget.Scale(
            orientation='h',
            min=0,
            max=100,
            step=1,
            value=20,
            on_change=lambda self: print(self.value),
            draw_value=True,
            value_pos='top'
        )
    """
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(
        self,
        orientation: str = "h",
        min: float = 0,
        max: float = 100,
        step: float = 1,
        value: float = 0,
        on_change: callable = None,
        draw_value: bool = False,
        value_pos: str = "top",
        **kwargs,
    ):
        self._adjustment = Gtk.Adjustment(0, 0, 0, 0, 0, 0)
        Gtk.Scale.__init__(self, adjustment=self._adjustment)
        BaseWidget.__init__(self, **kwargs)

        self._dragging = False
        self._on_change = None

        self.orientation = orientation
        self.min = min
        self.max = max
        self.step = step
        self.value = value
        self.on_change = on_change
        self.draw_value = draw_value
        self.value_pos = value_pos
        self.connect("value-changed", lambda x: self.__invoke_on_change())

    def set_property(self, property_name: str, value: Any) -> None:
        if property_name == "value_pos":
            super().set_value_pos(VALUE_POS[value])
        elif property_name == "orientation":
            super().set_property("orientation", ORIENTATION[value])
        else:
            super().set_property(property_name, value)

    @GObject.Property
    def value(self) -> float:
        return self.get_value()

    @value.setter
    def value(self, value: float) -> None:
        if not self._dragging:
            self._adjustment.set_value(value)

    @GObject.Property
    def min(self) -> float:
        return self._adjustment.props.lower

    @min.setter
    def min(self, value: float) -> None:
        self._adjustment.props.lower = value

    @GObject.Property
    def max(self) -> float:
        return self._adjustment.props.upper

    @max.setter
    def max(self, value: float) -> None:
        self._adjustment.props.upper = value

    @GObject.Property
    def on_change(self) -> callable:
        return self._on_change

    @on_change.setter
    def on_change(self, value: callable) -> None:
        self._on_change = value

    def __invoke_on_change(self):
        if self._dragging and self.on_change:
            self.on_change(self)

    @GObject.Property
    def step(self) -> float:
        return self._adjustment.props.step_increment

    @step.setter
    def step(self, value: float) -> None:
        self._adjustment.props.step_increment = value

    def do_button_press_event(self, event):
        self._dragging = True
        return Gtk.Widget.do_button_press_event(self, event)

    def do_button_release_event(self, event):
        self._dragging = False
        return Gtk.Widget.do_button_release_event(self, event)

    def do_key_press_event(self, event):
        self._dragging = True
        return Gtk.Widget.do_key_press_event(self, event)

    def do_key_release_event(self, event):
        self._dragging = False
        return Gtk.Widget.do_key_release_event(self, event)

    def do_scroll_event(self, event):
        self._dragging = True
        if event.delta_y > 0:
            super().set_value(self.value - self.step)            
        else:
            super().set_value(self.value + self.step)

        self._dragging = False
        return Gtk.Widget.do_scroll_event(self, event)

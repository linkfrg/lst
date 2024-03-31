from gi.repository import Gtk, GObject
from lst.widgets.widget import Widget

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


class Scale(Gtk.Scale, Widget):
    __gproperties__ = {**Widget.gproperties}

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
        self._dragging = False
        self._adjustment = Gtk.Adjustment(0, 0, 100, 1, 1, 0)
        Gtk.Scale.__init__(
            self,
            orientation=ORIENTATION[orientation],
            adjustment=self._adjustment,
        )
        Widget.__init__(self, **kwargs)

        self.set_value_pos(value_pos)
        self.set_draw_value(draw_value)
        self._on_change = None
        self.on_change = on_change
        self.step = step
        self.value = value
        self.min = min
        self.max = max
        self.connect("value-changed", lambda x: self.__invoke_on_change())

    @GObject.Property
    def value(self) -> float:
        return self.get_value()

    @value.setter
    def value(self, value: float) -> None:
        if not self._dragging:
            self._adjustment.set_value(value)

    def set_value(self, value: float) -> None:
        self.value = value

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

    def set_value_pos(self, value: str) -> None:
        return super().set_value_pos(VALUE_POS[value])

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

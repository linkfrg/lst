from gi.repository import Gtk, Gdk, GObject
from lst.widgets.widget import Widget


class Button(Gtk.Button, Widget):
    __gproperties__ = {**Widget.gproperties}

    def __init__(
        self,
        child: Gtk.Widget = None,
        on_click: callable = None,
        on_right_click: callable = None,
        on_middle_click: callable = None,
        on_hover: callable = None,
        on_hover_lost: callable = None,
        on_scroll_up: callable = None,
        on_scroll_down: callable = None,
        **kwargs,
    ):
        Gtk.Button.__init__(self)
        Widget.__init__(self, **kwargs)

        self._child = None
        self._on_click = None
        self._on_right_click = None
        self._on_middle_click = None
        self._on_hover = None
        self._on_hover_lost = None
        self._on_scroll_up = None
        self._on_scroll_down = None

        self.child = child
        self.on_click = on_click
        self.on_right_click = on_right_click
        self.on_middle_click = on_middle_click
        self.on_hover = on_hover
        self.on_hover_lost = on_hover_lost
        self.on_scroll_up = on_scroll_up
        self.on_scroll_down = on_scroll_down

        self.add_events(Gdk.EventMask.SCROLL_MASK)

        if on_hover:
            self.connect(
                "enter-notify-event", lambda x, event: self.on_hover(self, event)
            )

        if on_hover_lost:
            self.connect(
                "leave-notify-event", lambda x, event: self.on_hover_lost(self, event)
            )

        if on_click:
            self.connect(
                "button-press-event",
                lambda x, event: self.on_click(self, event)
                if event.button == 1
                else None,
            )

        if on_right_click:
            self.connect(
                "button-press-event",
                lambda x, event: self.on_right_click(self, event)
                if event.button == 2
                else None,
            )

        if on_middle_click:
            self.connect(
                "button-press-event",
                lambda x, event: self.on_middle_click(self, event)
                if event.button == 3
                else None,
            )

        if on_scroll_up:
            self.connect(
                "scroll-event",
                lambda x, event: self.on_scroll_up(self, event)
                if event.direction == Gdk.ScrollDirection.UP
                else None,
            )

        if on_scroll_down:
            self.connect(
                "scroll-event",
                lambda x, event: self.on_scroll_down(self, event)
                if event.direction == Gdk.ScrollDirection.DOWN
                else None,
            )

    @GObject.Property
    def child(self) -> Gtk.Widget:
        return self._child

    @GObject.Property
    def on_click(self) -> callable:
        return self._on_click

    @GObject.Property
    def on_right_click(self) -> callable:
        return self._on_right_click

    @GObject.Property
    def on_middle_click(self) -> callable:
        return self._on_middle_click

    @GObject.Property
    def on_hover(self) -> callable:
        return self._on_hover

    @GObject.Property
    def on_hover_lost(self) -> callable:
        return self._on_hover_lost

    @GObject.Property
    def on_scroll_up(self) -> callable:
        return self._on_scroll_up

    @GObject.Property
    def on_scroll_down(self) -> callable:
        return self._on_scroll_down

    @child.setter
    def child(self, child: Gtk.Widget) -> None:
        if child:
            if self.get_children() != []:
                self.remove(self.get_children()[0])
            self.add(child)
            self._child = child

    @on_click.setter
    def on_click(self, on_click: callable) -> None:
        self._on_click = on_click

    @on_right_click.setter
    def on_right_click(self, on_right_click: callable) -> None:
        self._on_right_click = on_right_click

    @on_middle_click.setter
    def on_middle_click(self, on_middle_click: callable) -> None:
        self._on_middle_click = on_middle_click

    @on_hover.setter
    def on_hover(self, on_hover: callable) -> None:
        self._on_hover = on_hover

    @on_hover_lost.setter
    def on_hover_lost(self, on_hover_lost: callable) -> None:
        self._on_hover_lost = on_hover_lost

    @on_scroll_up.setter
    def on_scroll_up(self, on_scroll_up: callable) -> None:
        self._on_scroll_up = on_scroll_up

    @on_scroll_down.setter
    def on_scroll_down(self, on_scroll_down: callable) -> None:
        self._on_scroll_down = on_scroll_down

    def set_on_click(self, on_click: callable) -> None:
        self.on_click = on_click

    def set_on_right_click(self, on_right_click: callable) -> None:
        self.on_right_click = on_right_click

    def set_on_middle_click(self, on_middle_click: callable) -> None:
        self.on_middle_click = on_middle_click

    def set_on_hover(self, on_hover: callable) -> None:
        self.on_hover = on_hover

    def set_on_hover_lost(self, on_hover_lost: callable) -> None:
        self.on_hover_lost = on_hover_lost

    def set_on_scroll_up(self, on_scroll_up: callable) -> None:
        self.on_scroll_up = on_scroll_up

    def set_on_scroll_down(self, on_scroll_down: callable) -> None:
        self.on_scroll_down = on_scroll_down

    def set_child(self, child: Gtk.Widget) -> None:
        self.child = child

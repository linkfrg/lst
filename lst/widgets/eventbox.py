from gi.repository import Gtk, Gdk, GObject
from lst.base_widget import BaseWidget


class EventBox(Gtk.EventBox, BaseWidget):
    """
    Bases: `Gtk.EventBox <https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/EventBox.html>`_, :class:`~lst.base_widget.BaseWidget`.
    
    A container that can receive events.

    Parameters:
        child (``Gtk.Widget``, optional): The child widget.
        on_click (``callable``, optional): The function to call on left click. 
        on_right_click (``callable``, optional): The function to call on right click. 
        on_middle_click (``callable``, optional): The function to call on middle click. 
        on_hover (``callable``, optional): The function to call on hover.
        on_hover_lost (``callable``, optional): The function to call on hover lost.
        on_scroll_up (``callable``, optional): The function to call on scroll up.
        on_scroll_down (``callable``, optional): The function to call on scroll down.

    .. code-block:: python

        Widget.EventBox(
            child=Widget.Label('button'),
            on_click=lambda self, event: print(self, event),
            on_right_click=lambda self, event: print(self, event),
            on_middle_click=lambda self, event: print(self, event),
            on_hover=lambda self, event: print(self, event),
            on_hover_lost=lambda self, event: print(self, event),
            on_scroll_up=lambda self, event: print(self, event),
            on_scroll_down=lambda self, event: print(self, event)
        )

    """
    __gproperties__ = {**BaseWidget.gproperties}

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
        Gtk.EventBox.__init__(self)
        BaseWidget.__init__(self, **kwargs)

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

        self.connect(
            "enter-notify-event",
            lambda x, event: self.on_hover(self, event) if self.on_hover else None,
        )

        self.connect(
            "leave-notify-event",
            lambda x, event: self.on_hover_lost(self, event)
            if self.on_hover_lost
            else None,
        )

        self.connect("button-press-event", self.__on_click)
        self.connect("scroll-event", self.__on_scroll)

    def __on_click(self, x, event) -> None:
        if event.button == 1 and self.on_click:
            self.on_click(self, event)
        elif event.button == 2 and self.on_right_click:
            self.on_right_click(self, event)
        elif event.button == 3 and self.on_middle_click:
            self.on_middle_click(self, event)

    def __on_scroll(self, x, event):
        if event.direction == Gdk.ScrollDirection.UP and self.on_scroll_up:
            self.on_scroll_up(self, event)
        elif event.direction == Gdk.ScrollDirection.DOWN and self.on_scroll_down:
            self.on_scroll_down(self, event)

    @GObject.Property
    def child(self) -> Gtk.Widget:
        if self.get_children() != []:
            return self.get_children()[0]

    @child.setter
    def child(self, child: Gtk.Widget) -> None:
        if self.get_children() != []:
            self.remove(self.get_children()[0])
        if child:
            self.add(child)

    @GObject.Property
    def on_click(self) -> callable:
        return self._on_click

    @on_click.setter
    def on_click(self, on_click: callable) -> None:
        self._on_click = on_click

    @GObject.Property
    def on_right_click(self) -> callable:
        return self._on_right_click

    @on_right_click.setter
    def on_right_click(self, on_right_click: callable) -> None:
        self._on_right_click = on_right_click

    @GObject.Property
    def on_middle_click(self) -> callable:
        return self._on_middle_click

    @on_middle_click.setter
    def on_middle_click(self, on_middle_click: callable) -> None:
        self._on_middle_click = on_middle_click

    @GObject.Property
    def on_hover(self) -> callable:
        return self._on_hover

    @on_hover.setter
    def on_hover(self, on_hover: callable) -> None:
        self._on_hover = on_hover

    @GObject.Property
    def on_hover_lost(self) -> callable:
        return self._on_hover_lost

    @on_hover_lost.setter
    def on_hover_lost(self, on_hover_lost: callable) -> None:
        self._on_hover_lost = on_hover_lost

    @GObject.Property
    def on_scroll_up(self) -> callable:
        return self._on_scroll_up

    @on_scroll_up.setter
    def on_scroll_up(self, on_scroll_up: callable) -> None:
        self._on_scroll_up = on_scroll_up

    @GObject.Property
    def on_scroll_down(self) -> callable:
        return self._on_scroll_down

    @on_scroll_down.setter
    def on_scroll_down(self, on_scroll_down: callable) -> None:
        self._on_scroll_down = on_scroll_down

from gi.repository import Gtk
from lst.base_widget import BaseWidget


class Calendar(Gtk.Calendar, BaseWidget):
    """
    Bases: `Gtk.Button <https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Button.html>`_, :class:`~lst.base_widget.BaseWidget`.

    A calendar.

    .. code-block:: python
    
        Widget.Calendar(
            day=1,
            month=1,
            year=2024,
            no_month_change=False,
            show_day_names=True,
            show_details=True,
            show_heading=True,
            show_week_numbers=True
        )
    
    """

    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(
        self,
        **kwargs,
    ):
        Gtk.Calendar.__init__(self)
        BaseWidget.__init__(self, **kwargs)

from gi.repository import Gtk
from lst.widgets.widget import Widget


class Calendar(Gtk.Calendar, Widget):
    __gproperties__ = {
        **Widget.gproperties
    }
    def __init__(
        self,
        no_month_change: bool = False,
        show_day_names: bool = True,
        show_details: bool = False,
        show_heading: bool = True,
        day: int = None,
        month: int = None,
        year: int = None,
        **kwargs
    ):
        Gtk.Calendar.__init__(self)
        Widget.__init__(self, **kwargs)

        self.no_month_change = no_month_change
        self.show_day_names = show_day_names
        self.show_details = show_details
        self.show_heading = show_heading

        if day:
            self.select_day(day)

        if month:
            self.select_month(month, self.get_date()[0])

        if year:
            self.select_month(self.get_date()[1], year)
        
from gi.repository import Gtk
from lst.widgets.widget import Widget

class RadioButton(Gtk.RadioButton, Widget):
    __gproperties__ = {**Widget.gproperties}

    def __init__(self, group: Gtk.RadioButton = None, label: str = None, **kwargs):
        self.new_with_label_from_widget(group, label)
        Widget.__init__(self, **kwargs)

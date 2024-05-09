from gi.repository import Gtk, GObject
from lst.base_widget import BaseWidget

class RadioButton(Gtk.RadioButton, BaseWidget):
    """
    Bases: `Gtk.RadioButton <https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/RadioButton.html>`_, :class:`~lst.base_widget.BaseWidget`.
    
    A radio button.
    
    .. code-block:: python

        Widget.RadioButton(
            group=Widget.RadioButton(label='radiobutton 1'),
            label='radiobutton 2',
            active=True,
        )
    
    """
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(self, on_toggled: callable = None, **kwargs):
        Gtk.RadioButton.__init__(self)
        BaseWidget.__init__(self, **kwargs)
        self._on_toggled = on_toggled
        self.connect('toggled', lambda x: self.on_toggled(x) if self.on_toggled else None)
    
    @GObject.Property
    def on_toggled(self) -> callable:
        return self._on_toggled

    @on_toggled.setter
    def on_toggled(self, value: callable) -> None:
        self._on_toggled = value
    
from gi.repository import Gtk, GObject
from lst.base_widget import BaseWidget

class FileChooserButton(Gtk.FileChooserButton, BaseWidget):
    """
    Bases: `Gtk.FileChooserButton <https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/FileChooserButton.html>`_, :class:`~lst.base_widget.BaseWidget`.
    
    A button that allow user select a file.

    Parameters:
        on_file_set(``callable``, optional): The function to call when the user selects a file.
    
    .. code-block :: python

        Widget.FileChooserButton(
            on_file_set=lambda self: print(self),
            title='hehe haha'
        )
    
    
    """
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(self, on_file_set: callable = None, **kwargs):
        Gtk.FileChooserButton.__init__(self)
        BaseWidget.__init__(self, **kwargs)
        self._on_file_set = on_file_set
        self.connect('file-set', lambda x: self.on_file_set(x) if self.on_file_set else None)

    @GObject.Property
    def on_file_set(self) -> callable:
        return self._on_file_set
    
    @on_file_set.setter
    def on_file_set(self, value: callable) -> None:
        self._on_file_set = value

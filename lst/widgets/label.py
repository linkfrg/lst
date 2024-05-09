from gi.repository import Gtk, Pango
from lst.base_widget import BaseWidget
from typing import Any

JUSTIFY = {
    'left': Gtk.Justification.LEFT,
    'right': Gtk.Justification.RIGHT,
    'center': Gtk.Justification.CENTER,
    'fill': Gtk.Justification.FILL,
}

WRAP_MODE = {
    "word": Pango.WrapMode.WORD,
    "char": Pango.WrapMode.CHAR,
    "word_char": Pango.WrapMode.WORD_CHAR,
}

ELLIPSIZE = {
    "none": Pango.EllipsizeMode.NONE,
    "start": Pango.EllipsizeMode.START,
    "middle": Pango.EllipsizeMode.MIDDLE,
    "end": Pango.EllipsizeMode.END
}

class Label(Gtk.Label, BaseWidget):
    """
    Bases: `Gtk.Label <https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Label.html>`_, :class:`~lst.base_widget.BaseWidget`.

    A widget that displays a small amount of text.

    Parameters:
        justify(``str``, optional): The alignment of the lines in the text of the label relative to each other. 
        This does NOT affect the alignment of the label within its allocation. 
        Possible values: ``"left"``, ``"right"``, ``"center"``, ``"fill"``.
        ellipsize(``str``, optional): The preferred place to ellipsize the string. Possible values: ``"none"``, ``"start"``, ``"middle"``, ``"end"``.
        wrap_mode(``str``, optional): If wrap is set, controls how linewrapping is done. Possible values: ``"word"``, ``"char"``, ``"word_char"``.
    
    .. code-block:: python
    
        Widget.Label(
            label='heh',
            use_markup=False,
            justify='left',
            wrap=True,
            wrap_mode='word',
            ellipsize='end',
            max_width_chars=52
        )
    
    """
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(self, **kwargs):
        Gtk.Label.__init__(self)
        BaseWidget.__init__(self, **kwargs)
    
    def set_property(self, property_name: str, value: Any) -> None:
        if property_name == "justify":
            super().set_property(property_name, JUSTIFY[value])
        elif property_name == "wrap_mode":
            super().set_property(property_name, WRAP_MODE[value])
        elif property_name == "ellipsize":
            super().set_property(property_name, ELLIPSIZE[value])
        else:
            super().set_property(property_name, value)
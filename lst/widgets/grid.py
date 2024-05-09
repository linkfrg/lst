from gi.repository import Gtk, GObject
from lst.base_widget import BaseWidget
from typing import List

class Grid(Gtk.Grid, BaseWidget):
    """
    Bases: `Gtk.Grid <https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Grid.html>`_, :class:`~lst.base_widget.BaseWidget`.
    
    A container which arranges its child widgets in rows and columns.

    Parameters:
        child(``List[Gtk.Widget]``, optional): The list of child widgets.
        column_num(``int``, optional): Number of columns.
        row_num(``int``, optional): Number of rows. Will not have effect if ``column_num`` is passed.
    
    .. code-block:: python

        Widget.Grid(
            child=[Widget.Label(123), Widget.Label('test')],
            column_num=3
        )
    
    .. code-block:: python

        Widget.Grid(
            child=[Widget.Label(123), Widget.Label('test')],
            row_num=3
        )

    """
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(
        self,
        child: List[Gtk.Widget] = None,
        column_num: int = None,
        row_num: int = None,
        **kwargs
    ):
        Gtk.Grid.__init__(self)
        BaseWidget.__init__(self, **kwargs)
        self._column_num = None
        self._row_num = None

        self.column_num = column_num
        self.row_num = row_num
        self.child = child

    @GObject.Property
    def column_num(self) -> int:
        return self._column_num
    
    @column_num.setter
    def column_num(self, value: int) -> None:
        self._column_num = value

    @GObject.Property
    def row_num(self) -> int:
        return self._row_num
    
    @row_num.setter
    def row_num(self, value: int) -> None:
        self._row_num = value

    @GObject.Property
    def child(self) -> list:
        return self.get_children()

    @child.setter
    def child(self, child: list) -> None:
        for c in self.get_children():
            self.remove(c)
        if child:
            if self.column_num:
                for i, c in enumerate(child):
                    self.attach(c, i % self.column_num, i // self.column_num, 1, 1)
            elif self.row_num:
                for i, c in enumerate(child):
                    self.attach(c, i // self.row_num, i % self.row_num, 1, 1)
            else:
                for c in child:
                    if c:   
                        self.add(c)

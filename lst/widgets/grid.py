from gi.repository import Gtk, GObject
from lst.widgets.widget import Widget
from typing import List

class Grid(Gtk.Grid, Widget):
    __gproperties__ = {**Widget.gproperties}

    def __init__(
        self,
        child: List[Gtk.Widget] = None,
        column_num: int = None,
        row_num: int = None,
        column_homogeneous: bool = False,
        row_homogeneous: bool = False,
        column_spacing: int = 0,
        row_spacing: int = 0,
        **kwargs
    ):
        Gtk.Grid.__init__(self)
        Widget.__init__(self, **kwargs)
        self._column_num = None
        self._row_num = None

        self.column_num = column_num
        self.row_num = row_num
        self.child = child
        self.set_column_homogeneous(column_homogeneous)
        self.set_row_homogeneous(row_homogeneous)
        self.set_column_spacing(column_spacing)
        self.set_row_spacing(row_spacing)

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

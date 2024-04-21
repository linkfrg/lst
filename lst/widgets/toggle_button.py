from gi.repository import GObject, Gtk
from lst.widgets.button import Button

class ToggleButton(Button):
    def __init__(
        self,
        child: Gtk.Widget = None,
        active: bool = False,
        on_activate: callable = None,
        on_deactivate: callable = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.on_activate = on_activate
        self.on_deactivate = on_deactivate
        self.active = active
        self.child = child
        self.connect('clicked', lambda *args: self.__callback())

    def __callback(self) -> None:
        if self.active:
            if self.on_deactivate:
                self.on_deactivate(self)
        else:
            if self.on_activate:
                self.on_activate(self)

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
    def on_activate(self) -> callable:
        return self._on_activate
    
    @on_activate.setter
    def on_activate(self, value: callable) -> None:
        self._on_activate = value

    @GObject.Property
    def on_deactivate(self) -> callable:
        return self._on_deactivate
    
    @on_deactivate.setter
    def on_deactivate(self, value: callable) -> None:
        self._on_deactivate = value

    @GObject.Property
    def active(self) -> bool:
        return self._active
    
    @active.setter
    def active(self, value: bool) -> None:
        self._active = value
        if value:
            self.add_class_name('active')
        else:
            self.remove_class_name('active')
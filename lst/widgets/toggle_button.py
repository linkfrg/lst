from lst.widgets.button import Button
from gi.repository import GObject, Gtk


class ToggleButton(Button):
    def __init__(self, child: Gtk.Widget = None, active: bool = False, on_activate: callable = None, on_deactivate: callable = None, **kwargs) -> None:
        super().__init__(child=child, on_click=lambda x, event: self.__callback(event), **kwargs)
        self.on_activate = on_activate
        self.on_deactivate = on_deactivate
        self.active = active

    def __callback(self, event) -> None:
        if self.active:
            if self.on_deactivate:
                self.on_deactivate(self, event)
        else:
            if self.on_activate:
                self.on_activate(self, event)
    
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

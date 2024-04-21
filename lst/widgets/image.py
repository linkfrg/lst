import os
from lst.widgets.widget import Widget
from gi.repository import Gtk, GdkPixbuf, GObject
from typing import Union


class Image(Gtk.Image, Widget):
    __gproperties__ = {**Widget.gproperties}

    def __init__(
        self, image: Union[str, GdkPixbuf.Pixbuf] = None, size: int = 16, **kwargs
    ):
        Gtk.Image.__init__(self)
        Widget.__init__(self, **kwargs)

        self._image = None
        self._size = None

        self.image = image
        self.size = size

    @GObject.Property
    def image(self) -> Union[str, GdkPixbuf.Pixbuf]:
        return self._image

    @image.setter
    def image(self, value: Union[str, GdkPixbuf.Pixbuf]) -> None:
        if isinstance(value, GdkPixbuf.Pixbuf):
            self.set_from_pixbuf(pixbuf=value)

        elif isinstance(value, str):
            if os.path.isfile(value):
                self.set_from_file(filename=value)
            else:
                self.set_from_icon_name(
                    icon_name=value, size=Gtk.IconSize.from_name(value)
                )

        else:
            self.set_from_icon_name(
                icon_name="image-missing", size=Gtk.IconSize.from_name("image-missing")
            )

        self._image = value
        self.size = self.size

    @GObject.Property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, value: int) -> None:
        if value:
            if isinstance(self._image, GdkPixbuf.Pixbuf):
                scalled_image = self._image.scale_simple(
                    value, value, GdkPixbuf.InterpType.BILINEAR
                )
                self.set_from_pixbuf(pixbuf=scalled_image)

            elif isinstance(self._image, str):
                if os.path.isfile(self._image):
                    scalled_image = GdkPixbuf.Pixbuf.new_from_file(
                        self._image
                    ).scale_simple(value, value, GdkPixbuf.InterpType.BILINEAR)
                    self.set_from_pixbuf(pixbuf=scalled_image)
                else:
                    self.set_pixel_size(value)

        self._size = value

import os
from lst.base_widget import BaseWidget
from gi.repository import Gtk, GdkPixbuf, GObject
from typing import Union, Any


class Image(Gtk.Image, BaseWidget):
    """
    Bases: `Gtk.Image <https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Image.html>`_, :class:`~lst.base_widget.BaseWidget`.

    An image widget. You can pass icon name, path to image or GdkPixbuf.

    Parameters:
        image(``Union[str, GdkPixbuf.Pixbuf]``, optional): Icon name, path to image or ``GdkPixbuf.Pixbuf``.
        pixel_size(``int``, optional): Size of icon. Work if image setted from icon name.
        width(``int``, optional): Width of image. Work if image setted from path or ``GdkPixbuf.Pixbuf``.
        height(``int``, optional): Height of image. Work if image setted from path or ``GdkPixbuf.Pixbuf``.

    .. hint::
        if it is unknown whether the image is the path, icon name or GdkPixbuf
        you can pass ``pixel_size``, ``width``, ``height`` together.

        .. code-block:: python

            Widget.Image(
                image=notification.icon,
                pixel_size=16,
                width=16,
                height=16
            )

    .. code-block:: python

        Widget.Image(
            image='audio-volume-high',
            pixel_size=12
        )
    
    .. code-block:: python

        Widget.Image(
            image='path/to/img',
            width=20,
            height=30
        )
    """
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(
        self,
        image: Union[str, GdkPixbuf.Pixbuf] = None,
        pixel_size: int = 16,
        width: int = 16,
        height: int = 16,
        **kwargs,
    ):
        Gtk.Image.__init__(self)
        BaseWidget.__init__(self, **kwargs)

        self._image = None
        self._width = width
        self._height = height
        self._type = None

        self.image = image
        self.pixel_size = pixel_size

    def __get_image_type(self, image: Any) -> str:
        if isinstance(image, GdkPixbuf.Pixbuf):
            return "pixbuf"
        elif isinstance(image, str):
            if os.path.isfile(image):
                return "file"
            else:
                return "icon"
        else:
            return None

    @GObject.Property
    def image(self) -> Union[str, GdkPixbuf.Pixbuf]:
        return self._image

    @image.setter
    def image(self, value: Union[str, GdkPixbuf.Pixbuf]) -> None:
        self._type = self.__get_image_type(value)

        if self._type == "pixbuf":
            self.set_from_pixbuf(pixbuf=value)

        elif self._type == "file":
            self.set_from_file(filename=value)

        elif self._type == "icon":
            self.set_from_icon_name(icon_name=value, size=Gtk.IconSize.from_name(value))
        else:
            self.set_from_icon_name(
                icon_name="image-missing", size=Gtk.IconSize.from_name("image-missing")
            )
            self._type = "icon"

        self._image = value
        self.pixel_size = self.pixel_size
        self.height = self._height
        self.width = self._width

    @GObject.Property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, value: int) -> None:
        if value:
            if self._type == "pixbuf":
                scalled_image = self._image.scale_simple(
                    self.width, value, GdkPixbuf.InterpType.BILINEAR
                )
                self.set_from_pixbuf(pixbuf=scalled_image)

            elif self._type == "file":
                scalled_image = GdkPixbuf.Pixbuf.new_from_file(
                    self._image
                ).scale_simple(self.width, value, GdkPixbuf.InterpType.BILINEAR)
                self.set_from_pixbuf(pixbuf=scalled_image)

            self._height = value

    @GObject.Property
    def width(self) -> int:
        return self._height

    @width.setter
    def width(self, value: int) -> None:
        if value:
            if self._type == "pixbuf":
                scalled_image = self._image.scale_simple(
                    value, self.height, GdkPixbuf.InterpType.BILINEAR
                )
                self.set_from_pixbuf(pixbuf=scalled_image)

            elif self._type == "file":
                scalled_image = GdkPixbuf.Pixbuf.new_from_file(
                    self._image
                ).scale_simple(value, self.height, GdkPixbuf.InterpType.BILINEAR)
                self.set_from_pixbuf(pixbuf=scalled_image)

            self._width = value

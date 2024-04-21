from lst.utils import load_interface_xml
from lst.dbus import DbusService, DbusClient
from gi.repository import Gio, GLib, GObject, DbusmenuGtk3, GdkPixbuf
from typing import Union
from lst.base_service import BaseService


class SystemTrayItem(BaseService):
    __gsignals__ = {
        "changed": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
        "removed": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def __init__(self, name: str, object_path: str):
        super().__init__()

        self._title = None
        self._icon = None
        self._tooltip = None
        self._status = None

        self.__dbus = DbusClient(
            name=name,
            object_path=object_path,
            interface_name="org.kde.StatusNotifierItem",
        )

        self.__dbus.watch_name(
            on_name_vanished=self.__removed,
        )

        dbus_menu = self.__dbus.get_dbus_property("Menu")
        self._menu = (
            DbusmenuGtk3.Menu(dbus_name=self.__dbus.name, dbus_object=dbus_menu)
            if dbus_menu
            else None
        )

        for signal_name in [
            "NewTitle",
            "NewIcon",
            "NewAttentionIcon",
            "NewOverlayIcon",
            "NewToolTip",
            "NewStatus",
        ]:
            self.__dbus.signal_subscribe(
                signal_name=signal_name, callback=self.__sync
            )
        self.__sync()

    def __sync(self, *args) -> None:
        icon_name = self.__dbus.get_dbus_property("IconName")
        attention_icon_name = self.__dbus.get_dbus_property("AttentionIconName")
        icon_pixmap = self.__dbus.get_dbus_property("IconPixmap")
        attention_icon_pixmap = self.__dbus.get_dbus_property("AttentionIconPixmap")

        if icon_name:
            self._icon = icon_name

        elif attention_icon_name:
            self._icon = attention_icon_name

        elif icon_pixmap:
            self._icon = self.__get_pixbuf(icon_pixmap)

        elif attention_icon_pixmap:
            self._icon = self.__get_pixbuf(attention_icon_pixmap)

        else:
            self._icon = "image-missing"

        self._title = self.__dbus.get_dbus_property("Title")
        tooltip = self.__dbus.get_dbus_property("ToolTip")
        self._tooltip = self.title if not tooltip else tooltip[2]
        self._status = self.__dbus.get_dbus_property("Status")

        self.emit("changed")

    def __removed(self, *args) -> None:
        for signal_id in self.__dbus.subscribed_signals:
            self.__dbus.signal_unsubscribe(signal_id)
        self.__dbus.unwatch_name()
        self.emit("removed")

    @GObject.Property
    def id(self) -> str:
        return self.__dbus.get_dbus_property("Id")

    @GObject.Property
    def category(self) -> str:
        return self.__dbus.get_dbus_property("Category")

    @GObject.Property
    def title(self) -> str:
        return self._title

    @GObject.Property
    def status(self) -> str:
        return self._status

    @GObject.Property
    def window_id(self) -> int:
        return self.__dbus.get_dbus_property("WindowId")

    @GObject.Property
    def icon(self) -> Union[str, GdkPixbuf.Pixbuf]:
        return self._icon

    @GObject.Property
    def item_is_menu(self) -> bool:
        return self.__dbus.get_dbus_property("ItemIsMenu")

    @GObject.Property
    def menu(self) -> DbusmenuGtk3.Menu:
        return self._menu

    @GObject.Property
    def tooltip(self) -> str:
        return self._tooltip

    def __get_pixbuf(self, pixmap_array) -> GdkPixbuf.Pixbuf:
        pixmap = sorted(pixmap_array, key=lambda x: x[0])[-1]
        array = bytearray(pixmap[2])

        for i in range(0, 4 * pixmap[0] * pixmap[1], 4):
            alpha = array[i]
            array[i] = array[i + 1]
            array[i + 1] = array[i + 2]
            array[i + 2] = array[i + 3]
            array[i + 3] = alpha

        return GdkPixbuf.Pixbuf.new_from_bytes(
            GLib.Bytes.new(array),
            GdkPixbuf.Colorspace.RGB,
            True,
            8,
            pixmap[0],
            pixmap[1],
            pixmap[0] * 4,
        )


class SystemTrayService(BaseService):
    __gsignals__ = {
        "added": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, (GObject.Object,)),
        "removed": (
            GObject.SignalFlags.RUN_FIRST,
            GObject.TYPE_NONE,
            (GObject.Object,),
        ),
    }

    def __init__(self):
        super().__init__()

        self.__dbus = DbusService(
            name="org.kde.StatusNotifierWatcher",
            object_path="/StatusNotifierWatcher",
            xml=load_interface_xml("org.kde.StatusNotifierWatcher.xml"),
            on_name_lost=lambda x, y: print("Another system tray is already running"),
        )

        self.__dbus.register_dbus_property(
            name="ProtocolVersion", method=self.ProtocolVersion
        )
        self.__dbus.register_dbus_property(
            name="IsStatusNotifierHostRegistered",
            method=self.IsStatusNotifierHostRegistered,
        )
        self.__dbus.register_dbus_property(
            name="RegisteredStatusNotifierItems",
            method=self.RegisteredStatusNotifierItems,
        )

        self.__dbus.register_dbus_method(
            name="RegisterStatusNotifierItem", method=self.RegisterStatusNotifierItem
        )

        self._items = {}

    @GObject.Property
    def items(self) -> list:
        return list(self._items.values())

    def ProtocolVersion(self) -> GLib.Variant:
        return GLib.Variant("i", 0)

    def IsStatusNotifierHostRegistered(self) -> GLib.Variant:
        return GLib.Variant("b", True)

    def RegisteredStatusNotifierItems(self) -> GLib.Variant:
        return GLib.Variant("as", list(self._items.keys()))

    def RegisterStatusNotifierItem(
        self, invocation: Gio.DBusMethodInvocation, service: str
    ) -> None:
        if service.startswith("/"):
            object_path = invocation.get_sender()
            bus_name = service

        else:
            object_path = service
            bus_name = "/StatusNotifierItem"

        item = SystemTrayItem(object_path, bus_name)

        item.connect("removed", lambda x: self.__remove_item(bus_name))
        self._items[bus_name] = item
        self.emit("added", item)
        self.notify('items')

    def __remove_item(self, bus_name: str) -> None:
        item = self._items.pop(bus_name)
        self.emit("removed", item)
        self.notify('items')


system_tray = SystemTrayService()

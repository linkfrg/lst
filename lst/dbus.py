from gi.repository import Gio, GLib, GObject
import threading


class DbusService(GObject.Object):
    def __init__(
        self,
        name: str,
        object_path: str,
        xml: str,
        on_name_acquired: callable = None,
        on_name_lost: callable = None,
    ):
        super().__init__()
        Gio.bus_own_name(
            Gio.BusType.SESSION,
            name,
            Gio.BusNameOwnerFlags.NONE,
            lambda connection, name: self.__export_object(connection, xml),
            on_name_acquired,
            on_name_lost,
        )

        self._name = name
        self._object_path = object_path

        self._methods = {}
        self._properties = {}

    @GObject.Property
    def name(self) -> str:
        return self._name

    @GObject.Property
    def object_path(self) -> str:
        return self._object_path

    @GObject.Property
    def connection(self) -> Gio.DBusConnection:
        return self._connection

    @GObject.Property
    def methods(self) -> dict:
        return self._methods

    @GObject.Property
    def properties(self) -> dict:
        return self._properties

    def __export_object(self, connection, xml) -> None:
        self._connection = connection
        node = Gio.DBusNodeInfo.new_for_xml(xml)
        self._connection.register_object(
            self._object_path,
            node.interfaces[0],
            self.__handle_method_call,
            self.__handle_get_property,
            None,
        )

    def __handle_method_call(
        self,
        connection,
        sender,
        object_path,
        interface_name,
        method_name,
        params,
        invocation,
    ):
        def callback(func):
            result = func(invocation, *params)
            invocation.return_value(result)

        func = self._methods.get(method_name, None)
        if func:
            threading.Thread(target=lambda: callback(func)).start()

    def __handle_get_property(self, connection, sender, object_path, interface, value):
        func = self._properties.get(value, None)
        if func:
            return func()

    def register_dbus_method(self, name: str, method: callable) -> None:
        self._methods[name] = method

    def register_dbus_property(self, name: str, method: callable) -> None:
        self._properties[name] = method

    def emit_signal(self, signal_name: str, *args) -> None:
        self._connection.emit_signal(
            None,
            self._object_path,
            self._name,
            signal_name,
            *args,
        )


class DbusClient(GObject.Object):
    def __init__(
        self,
        name: str,
        object_path: str,
        interface_name: str,
    ):
        super().__init__()
        self._name = name
        self._object_path = object_path
        self._interface_name = interface_name

        self._subscribed_signals = []
        self._watcher = None

        self._proxy = Gio.DBusProxy.new_for_bus_sync(
            Gio.BusType.SESSION,
            Gio.DBusProxyFlags.NONE,
            None,
            self._name,
            self._object_path,
            self._interface_name,
            None,
        )
        self._connection = self._proxy.get_connection()

    @GObject.Property
    def proxy(self) -> Gio.DBusProxy:
        return self._proxy

    @GObject.Property
    def name(self) -> str:
        return self._name

    @GObject.Property
    def object_path(self) -> str:
        return self._object_path

    @GObject.Property
    def interface_name(self) -> str:
        return self._interface_name

    @GObject.Property
    def connection(self) -> Gio.DBusConnection:
        return self._connection

    @GObject.Property
    def subscribed_signals(self) -> str:
        return self._subscribed_signals

    @GObject.Property
    def watcher(self) -> int:
        return self._watcher

    def watch_name(
        self, on_name_appeared: callable = None, on_name_vanished: callable = None
    ) -> None:
        self._watcher = Gio.bus_watch_name(
            Gio.BusType.SESSION,
            self._name,
            Gio.BusNameWatcherFlags.NONE,
            on_name_appeared,
            on_name_vanished,
        )

    def unwatch_name(self) -> None:
        Gio.bus_unwatch_name(self._watcher)

    def signal_subscribe(
        self,
        signal_name: str,
        name: str = None,
        object_path: str = None,
        interface_name: str = None,
        callback: callable = None,
    ) -> None:
        signal = self._connection.signal_subscribe(
            self._name if not name else name,
            self._interface_name if not interface_name else interface_name,
            signal_name,
            self._object_path if not object_path else object_path,
            None,
            Gio.DBusSignalFlags.NONE,
            callback,
        )
        self._subscribed_signals.append(signal)

    def signal_unsubscribe(self, id: int) -> None:
        self._connection.signal_unsubscribe(id)

    def get_dbus_property(self, property_name: str):
        try:
            return self.call_sync(
                interface_name="org.freedesktop.DBus.Properties",
                method_name="Get",
                parameters=GLib.Variant(
                    "(ss)",
                    (self._interface_name, property_name),
                ),
            )[0]
        except GLib.GError:
            return None

    def call_sync(
        self,
        method_name: str,
        name: str = None,
        object_path: str = None,
        interface_name: str = None,
        parameters: GLib.Variant = None,
        reply_type: GLib.VariantType = None,
        timeout: int = -1,
    ) -> None:
        return self._connection.call_sync(
            self._name if not name else name,
            self._object_path if not object_path else object_path,
            self._interface_name if not interface_name else interface_name,
            method_name,
            parameters,
            reply_type,
            Gio.DBusCallFlags.NONE,
            timeout,
            None,
        )

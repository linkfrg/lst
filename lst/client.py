from lst.dbus import DbusClient
from lst.app import APP_INTERFACE_NAME, APP_OBJECT_PATH
from gi.repository import GLib


class LstClient:
    def __init__(self):
        self.__dbus = DbusClient(
            name=APP_INTERFACE_NAME,
            object_path=APP_OBJECT_PATH,
            interface_name=APP_INTERFACE_NAME,
        )

    def OpenWindow(self, window: str) -> None:
        self.__dbus.call_sync(
            method_name="OpenWindow",
            parameters=GLib.Variant(
                "(s)",
                (window,),
            ),
        )

    def CloseWindow(self, window: str) -> None:
        self.__dbus.call_sync(
            method_name="CloseWindow",
            parameters=GLib.Variant(
                "(s)",
                (window,),
            ),
        )

    def ToggleWindow(self, window: str) -> None:
        self.__dbus.call_sync(
            method_name="ToggleWindow",
            parameters=GLib.Variant(
                "(s)",
                (window,),
            ),
        )

    def ListWindows(self) -> None:
        response = self.__dbus.call_sync(
            method_name="ListWindows",
        )
        print('\n'.join(response[0]))

    def Quit(self) -> None:
        self.__dbus.call_sync(
            method_name="Quit",
        )

    def Inspector(self) -> None:
        self.__dbus.call_sync(
            method_name="Inspector",
        )

    def RunPython(self, code: str) -> None:
        self.__dbus.call_sync(
            method_name="RunPython",
            parameters=GLib.Variant(
                "(s)",
                (code,),
            ),
        )

    def RunFile(self, path: str) -> None:
        self.__dbus.call_sync(
            method_name="RunFile",
            parameters=GLib.Variant(
                "(s)",
                (path,),
            ),
        )

    def Reload(self) -> None:
        self.__dbus.call_sync(method_name="Reload")

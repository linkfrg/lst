import os
import sass
import sys
import traceback
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from lst.dbus import DbusService
from lst.utils import load_interface_xml
from gi.repository import Gtk, Gdk, Gio, GObject, GLib

APP_INTERFACE_NAME = "com.github.linkfrg.lst"
APP_OBJECT_PATH = "/com/github/linkfrg/lst"

class ConfigChangedHandler(FileSystemEventHandler, GObject.Object):
    __gsignals__ = {
        "changed": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def on_modified(self, event):
        self.reload_config(event)

    def on_created(self, event):
        self.reload_config(event)

    def on_deleted(self, event):
        self.reload_config(event)

    def reload_config(self, event):
        if not event.is_directory and "__pycache__" not in event.src_path:
            if os.path.splitext(event.src_path)[1] in (".py", ".scss", ".css"):
                self.emit("changed")


class LstApp(Gtk.Application):
    __gsignals__ = {
        "ready": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
        "quit": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def __init__(self):
        super().__init__(
            application_id=APP_INTERFACE_NAME,
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )

        self.__dbus = DbusService(
            name=APP_INTERFACE_NAME,
            object_path=APP_OBJECT_PATH,
            xml=load_interface_xml("com.github.linkfrg.lst.xml"),
        )

        self.__dbus.register_dbus_method(name='OpenWindow', method=self.OpenWindow)
        self.__dbus.register_dbus_method(name='CloseWindow', method=self.CloseWindow)
        self.__dbus.register_dbus_method(name='ToggleWindow', method=self.ToggleWindow)
        self.__dbus.register_dbus_method(name='Quit', method=self.Quit)
        self.__dbus.register_dbus_method(name='Inspector', method=self.Inspector)
        self.__dbus.register_dbus_method(name='RunPython', method=self.RunPython)
        self.__dbus.register_dbus_method(name='RunFile', method=self.RunFile)
        self.__dbus.register_dbus_method(name='Reload', method=self.Reload)
        self.__dbus.register_dbus_method(name='ListWindows', method=self.ListWindows)


        self._config_dir = None
        self._config_filename = None
        self._css_provider = None
        self._style_path = None
        self._windows = {}

    @GObject.Property
    def windows(self) -> dict:
        return self._windows

    def setup(self, config_dir: str, config_filename: str) -> None:
        self._config_dir = config_dir
        self._config_filename = config_filename

    def apply_css(self, style_path: str) -> None:
        self._style_path = style_path
        screen = Gdk.Screen.get_default()
        self._css_provider = Gtk.CssProvider()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(
            screen, self._css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        compiled_scss = sass.compile(filename=style_path)

        self._css_provider.load_from_data(compiled_scss)

    def remove_css(self) -> None:
        if self._css_provider:
            screen = Gdk.Screen.get_default()
            style_context = Gtk.StyleContext()
            style_context.remove_provider_for_screen(screen, self._css_provider)

    def reload_css(self) -> None:
        if self._css_provider:
            self.remove_css()
            self.apply_css(self._style_path)

    def do_activate(self) -> None:
        self.hold()

        event_handler = ConfigChangedHandler()
        event_handler.connect("changed", lambda x: self.reload())
        observer = Observer()
        observer.schedule(event_handler, path=self._config_dir, recursive=True)
        observer.start()

        sys.path.append(self._config_dir)
        try:
            __import__(self._config_filename)
            self.emit("ready")
        except Exception:
            traceback.print_exc()

    def get_window(self, window_name) -> Gtk.Window:
        window = self._windows.get(window_name, None)
        if window:
            return window
        else:
            print(f"No such window: {window_name}")

    def open_window(self, window_name: str) -> None:
        window = self.get_window(window_name)
        if window:
            window.visible = True

    def close_window(self, window_name: str) -> None:
        window = self.get_window(window_name)
        if window:
            window.visible = False

    def toggle_window(self, window_name: str) -> None:
        window = self.get_window(window_name)
        if window:
            window.visible = not window.visible
            return window.visible

    def add_window(self, window_name: str, window: Gtk.Window) -> None:
        self._windows[window_name] = window

    def reload(self) -> None:
        self.quit()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def quit(self) -> None:
        self.emit("quit")
        super().quit()

    def inspector(self) -> None:
        Gtk.Window.set_interactive_debugging(True)

    def ToggleWindow(self, invocation, window_name: str) -> GLib.Variant:
        def callback():
            self.toggle_window(window_name)
        GLib.idle_add(callback)

    def RunPython(self, invocation, code: str) -> None:
        eval(code)

    def RunFile(self, invocation, path: str) -> None:
        with open(path, "r") as file:
            code = file.read()
            exec(code)

    def Reload(self, invocation) -> None:
        invocation.return_value(None)
        self.reload()

    def ListWindows(self, invocation) -> str:
        return GLib.Variant("(as)", (tuple(self._windows),))
    
    def OpenWindow(self, invocation, window_name: str) -> None:
        GLib.idle_add(self.open_window, window_name)

    def CloseWindow(self, invocation, window_name: str) -> None:
        GLib.idle_add(self.close_window, window_name)

    def Quit(self, invocation) -> None:
        GLib.idle_add(self.quit)

    def Inspector(self, invocation) -> None:
        GLib.idle_add(self.inspector)


app = LstApp()
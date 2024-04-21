import os
import subprocess
from gi.repository import GObject, Gio, GLib
from lst.utils import read_json, write_json
from lst.base_service import BaseService
from typing import List

APPLICATIONS_CACHE_FILE = f"{GLib.get_user_cache_dir()}/lst/apps.json"
APPLICATIONS_EMPTY_CACHE_FILE = {"pinned": []}

class Application(BaseService):
    __gsignals__ = {
        "pinned": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
        "unpinned": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def __init__(self, app: Gio.DesktopAppInfo):
        self._app = app
        super().__init__()

    @GObject.Property
    def app(self) -> Gio.DesktopAppInfo:
        return self._app

    @GObject.Property
    def id(self) -> str:
        return self._app.get_id()

    @GObject.Property
    def name(self) -> str:
        return self._app.get_display_name()

    @GObject.Property
    def description(self) -> str:
        return self._app.get_description()

    @GObject.Property
    def icon(self) -> str:
        icon = self._app.get_string("Icon")
        if not icon:
            return 'image-missing'
        else:
            return icon

    @GObject.Property
    def keywords(self) -> str:
        return self._app.get_keywords()

    @GObject.Property
    def desktop_file(self) -> str:
        return os.path.basename(self._app.get_filename())

    @GObject.Property
    def executable(self) -> str:
        return self._app.get_executable()

    def launch(self) -> None:
        subprocess.Popen(
            f"gtk-launch {self.desktop_file}",
            shell=True,
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def pin(self) -> None:
        self.emit("pinned")

    def unpin(self) -> None:
        self.emit("unpinned")


class ApplicationsService(BaseService):
    __gsignals__ = {
        "all_apps_changed": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
        "pinned_apps_changed": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def __init__(self):
        super().__init__()
        self._apps = {}
        self._pinned = {}
        monitor = Gio.AppInfoMonitor.get() # TODO it don't work, need to directly monitor app dirs like /usr/share/applications
        monitor.connect("changed", lambda x: self.__sync())
        self.__sync()

    @GObject.Property
    def apps(self) -> List[Application]:
        return sorted(list(self._apps.values()), key=lambda x: x.name)

    @GObject.Property
    def pinned(self) -> List[Application]:
        return list(self._pinned.values())

    def __sync(self) -> None:
        for a in Gio.AppInfo.get_all():
            if not a.get_nodisplay():
                entry = Application(app=a)
                self.__connect_entry(entry)
                self._apps[entry.id] = entry

        self.__read_pinned_entries()
        self.emit("all_apps_changed")
        self.emit('pinned_apps_changed')
        self.notify('apps')
        self.notify('pinned')

    def __pin_entry(self, entry: Application) -> None:
        if entry.id in self._pinned:
            print(f"App {entry.name} already pinned!")
            return

        self._pinned[entry.id] = entry
        write_json(APPLICATIONS_CACHE_FILE, self.__generate_json())
        self.emit("pinned_apps_changed")
        self.notify('pinned')

    def __unpin_entry(self, entry: Application) -> None:
        self._pinned.pop(entry.id)
        write_json(APPLICATIONS_CACHE_FILE, self.__generate_json())
        self.emit("pinned_apps_changed")
        self.notify('pinned')

    def __read_pinned_entries(self) -> None:
        cache = read_json(APPLICATIONS_CACHE_FILE, APPLICATIONS_EMPTY_CACHE_FILE)
        for pinned in cache["pinned"]:
            app = Gio.DesktopAppInfo.new(desktop_id=pinned)
            entry = Application(
                app=app,
            )
            self.__connect_entry(entry)
            self._pinned[entry.id] = entry

    def filter_entries(self, query: str) -> List[Application]:
        return [
            entry
            for entry in self.apps
            if query.lower() in entry.name.lower()
            or (entry.description and query.lower() in entry.description.lower())
            or (entry.keywords and query.lower() in entry.keywords)
        ]

    def __connect_entry(self, entry: Application) -> None:
        entry.connect("pinned", lambda x: self.__pin_entry(x))
        entry.connect("unpinned", lambda x: self.__unpin_entry(x))

    def __generate_json(self) -> dict:
        return {
            "pinned": [p.id for p in self.pinned],
        }


applications = ApplicationsService()

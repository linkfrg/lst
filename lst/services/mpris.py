import shutil
import os
import requests
from lst.dbus import DbusClient
from gi.repository import GObject, GLib
from lst.services.base_service import BaseService

ART_URL_CACHE_DIR = f"{GLib.get_user_cache_dir()}/lst/art_url"

os.makedirs(ART_URL_CACHE_DIR, exist_ok=True)


class MprisPlayer(BaseService):
    __gsignals__ = {
        "closed": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
        "changed": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def __init__(self, name: str):
        super().__init__()
        self.__mpris_proxy = DbusClient(
            name=name,
            object_path="/org/mpris/MediaPlayer2",
            interface_name="org.mpris.MediaPlayer2",
        )
        self.__player_proxy = DbusClient(
            name=name,
            object_path="/org/mpris/MediaPlayer2",
            interface_name="org.mpris.MediaPlayer2.Player",
        )

        self.__player_proxy.proxy.connect(
            "g-properties-changed", lambda *args: self.__sync(*args)
        )

        self.__mpris_proxy.watch_name(
            on_name_vanished=lambda *args: self.emit("closed")
        )

        self._position = -1
        self._art_url = None
        self.__sync_position()
        self.__cache_art_url()

    def __sync(self, *args):
        metadata = args[1].unpack().get("Metadata", None)
        if metadata:
            if metadata.get("mpris:artUrl", None):
                self.__cache_art_url()
        self.emit("changed")
        self.notify_all(without="position")

    def __cache_art_url(self) -> None:
        if self.metadata:
            art_url = self.metadata.get("mpris:artUrl", None)
            if art_url:
                if art_url.startswith("file://"):
                    path = art_url.replace("file://", "")
                    result = ART_URL_CACHE_DIR + "/" + os.path.basename(path)
                    if not os.path.exists(result):
                        shutil.copy(path, result)
                elif art_url.startswith("https://") or art_url.startswith("http://"):
                    result = ART_URL_CACHE_DIR + "/" + os.path.basename(art_url)
                    if not os.path.exists(result):
                        response = requests.get(art_url)
                        if response.status_code == 200:
                            with open(
                                os.path.join(ART_URL_CACHE_DIR, os.path.basename(art_url)),
                                "wb",
                            ) as file:
                                file.write(response.content)
                        else:
                            print("Failed to download the file.")
                self._art_url = result

    def __sync_position(self) -> None:
        position = self.__player_proxy.get_dbus_property("Position")
        if position:
            self._position = position // 1_000_000
            self.notify("position")
        GLib.timeout_add_seconds(1, self.__sync_position)

    @GObject.Property
    def can_control(self) -> bool:
        return self.__player_proxy.get_dbus_property("CanControl")

    @GObject.Property
    def can_go_next(self) -> bool:
        return self.__player_proxy.get_dbus_property("CanGoNext")

    @GObject.Property
    def can_go_previous(self) -> bool:
        return self.__player_proxy.get_dbus_property("CanGoPrevious")

    @GObject.Property
    def can_pause(self) -> bool:
        return self.__player_proxy.get_dbus_property("CanPause")

    @GObject.Property
    def can_play(self) -> bool:
        return self.__player_proxy.get_dbus_property("CanPlay")

    @GObject.Property
    def can_seek(self) -> bool:
        return self.__player_proxy.get_dbus_property("CanSeek")

    @GObject.Property
    def loop_status(self) -> str:
        return self.__player_proxy.get_dbus_property("LoopStatus")

    @GObject.Property
    def metadata(self) -> dict:
        return self.__player_proxy.get_dbus_property("Metadata")

    @GObject.Property
    def track_id(self) -> str:
        return self.metadata.get("mpris:trackid", None)

    @GObject.Property
    def length(self) -> int:
        length = self.metadata.get("mpris:length", None)
        if length:
            return length // 1_000_000
        else:
            return -1

    @GObject.Property
    def art_url(self) -> str:
        return self._art_url

    @GObject.Property
    def album(self) -> str:
        return self.metadata.get("xesam:album", None)

    @GObject.Property
    def artist(self) -> str:
        artist = self.metadata.get("xesam:artist", None)
        if isinstance(artist, list):
            return "".join(artist)
        else:
            return artist

    @GObject.Property
    def title(self) -> str:
        return self.metadata.get("xesam:title", None)

    @GObject.Property
    def url(self) -> str:
        return self.metadata.get("xesam:url", None)

    @GObject.Property
    def playback_status(self) -> str:
        return self.__player_proxy.get_dbus_property("PlaybackStatus")

    @GObject.Property
    def position(self) -> int:
        return self._position

    @position.setter
    def position(self, value: int) -> None:
        self.__player_proxy.call_sync(
            "SetPosition",
            parameters=GLib.Variant("(ox)", (self.track_id, value * 1_000_000)),
        )

    def set_position(self, value: int) -> None:
        self.position = value

    @GObject.Property
    def shuffle(self) -> bool:
        return self.__player_proxy.get_dbus_property("Shuffle")

    @GObject.Property
    def volume(self) -> float:
        return self.__player_proxy.get_dbus_property("Volume")

    @GObject.Property
    def identity(self) -> str:
        return self.__mpris_proxy.get_dbus_property("Identity")

    @GObject.Property
    def desktop_entry(self) -> str:
        return self.__mpris_proxy.get_dbus_property("DesktopEntry")

    def next(self) -> None:
        self.__player_proxy.call_sync(method_name="Next")

    def pause(self) -> None:
        self.__player_proxy.call_sync(method_name="Pause")

    def play(self) -> None:
        self.__player_proxy.call_sync(method_name="Play")

    def play_pause(self) -> None:
        self.__player_proxy.call_sync(method_name="PlayPause")

    def previous(self) -> None:
        self.__player_proxy.call_sync(method_name="Previous")

    def stop(self) -> None:
        self.__player_proxy.call_sync(method_name="Stop")

    def seek(self, offset: int) -> None:
        self.__player_proxy.call_sync(
            method_name="Seek", parameters=GLib.Variant("(x)", (offset * 1_000_100,))
        )


class MprisService(BaseService):
    __gsignals__ = {
        "player_added": (
            GObject.SignalFlags.RUN_FIRST,
            GObject.TYPE_NONE,
            (GObject.Object,),
        ),
        "player_removed": (
            GObject.SignalFlags.RUN_FIRST,
            GObject.TYPE_NONE,
            (GObject.Object,),
        ),
        "players_changed": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def __init__(self):
        super().__init__()
        self.__dbus = DbusClient(
            name="org.freedesktop.DBus",
            object_path="/org/freedesktop/DBus",
            interface_name="org.freedesktop.DBus",
        )
        self.__players = {}
        self.__get_players()

        self.__dbus.signal_subscribe(
            signal_name="NameOwnerChanged",
            callback=lambda *args: self.__add_player(args[5][0]),
        )

    def __get_players(self) -> None:
        all_names = self.__dbus.call_sync("ListNames")[0]
        for name in all_names:
            self.__add_player(name)

    def __add_player(self, name: str) -> None:
        if (
            name.startswith("org.mpris.MediaPlayer2")
            and name not in self.__players
            and name != "org.mpris.MediaPlayer2.playerctld"
        ):
            player = MprisPlayer(name)
            self.__players[name] = player
            player.connect("closed", lambda x: self.__remove_player(name))
            self.notify("players")
            self.emit("players_changed")
            self.emit("player_added", player)

    def __remove_player(self, name: str) -> None:
        if name in self.__players:
            player = self.__players.pop(name)
            self.notify("players")
            self.emit("players_changed")
            self.emit('player_removed', player)

    @GObject.Property
    def players(self) -> list:
        return list(self.__players.values())


mpris = MprisService()

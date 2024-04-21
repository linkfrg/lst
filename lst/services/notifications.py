import datetime
import os
from lst.dbus import DbusService
from gi.repository import GLib, GObject, GdkPixbuf
from lst.utils import load_interface_xml, read_json, write_json
from lst.base_service import BaseService

NOTIFICATIONS_CACHE_DIR = f"{GLib.get_user_cache_dir()}/lst/notifications"
NOTIFICATIONS_CACHE_FILE = f"{NOTIFICATIONS_CACHE_DIR}/notifications.json"
NOTIFICATIONS_IMAGE_DATA = f"{NOTIFICATIONS_CACHE_DIR}/images"
NOTIFICATIONS_EMPTY_CACHE_FILE = {"notifications": [], "dnd": False}

os.makedirs(NOTIFICATIONS_CACHE_DIR, exist_ok=True)
os.makedirs(NOTIFICATIONS_IMAGE_DATA, exist_ok=True)

class Notification(BaseService):
    __gsignals__ = {
        "closed": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
        "dismissed": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
        "action_invoked": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, (str,)),
    }

    def __init__(
        self,
        id: int,
        app_name: str,
        icon: str,
        summary: str,
        body: str,
        actions: list,
        urgency: int,
        timeout: int,
        time: int,
        popup: bool,
    ):
        self._id = id
        self._app_name = app_name
        self._icon = icon
        self._summary = summary
        self._body = body
        self._actions = actions
        self._timeout = timeout
        self._time = time
        self._urgency = urgency
        self._popup = popup

        super().__init__()

        GLib.timeout_add_seconds(5, self.dismiss)

    @GObject.Property
    def id(self) -> int:
        return self._id

    @GObject.Property
    def app_name(self) -> str:
        return self._app_name

    @GObject.Property
    def icon(self) -> str:
        return self._icon

    @GObject.Property
    def summary(self) -> str:
        return self._summary

    @GObject.Property
    def body(self) -> str:
        return self._body

    @GObject.Property
    def actions(self) -> list:
        return self._actions

    @GObject.Property
    def timeout(self) -> int:
        return self._timeout

    @GObject.Property
    def time(self) -> int:
        return self._time

    @GObject.Property
    def urgency(self) -> int:
        return self._urgency

    @GObject.Property
    def popup(self) -> bool:
        return self._popup

    @GObject.Property
    def json(self) -> None:
        return {
            "id": self._id,
            "app_name": self._app_name,
            "icon": self._icon,
            "summary": self._summary,
            "body": self._body,
            "actions": self._actions,
            "timeout": self._timeout,
            "time": self._time,
            "urgency": self._urgency,
        }

    def close(self) -> None:
        self.emit("closed")

    def invoke_action(self, action: str) -> None:
        self.emit("action_invoked", action)

    def dismiss(self) -> None:
        if self._popup:
            self._popup = False
            self.emit("dismissed")
            self.notify("popup")


class NotificationService(BaseService):
    __gsignals__ = {
        "notified": (
            GObject.SignalFlags.RUN_FIRST,
            GObject.TYPE_NONE,
            (GObject.Object,),
        ),
        "new_popup": (
            GObject.SignalFlags.RUN_FIRST,
            GObject.TYPE_NONE,
            (GObject.Object,),
        ),
        "closed": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, (GObject.Object,)),
        "dismissed": (
            GObject.SignalFlags.RUN_FIRST,
            GObject.TYPE_NONE,
            (GObject.Object,),
        ),
        "toggled_dnd": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, (bool,)),
    }

    def __init__(self):
        super().__init__()

        self.__dbus = DbusService(
            name="org.freedesktop.Notifications",
            object_path="/org/freedesktop/Notifications",
            xml=load_interface_xml("org.freedesktop.Notifications.xml"),
            on_name_lost=lambda x, y: print(
                "Another notification daemon is already running"
            ),
        )

        self.__dbus.register_dbus_method(
            name="GetServerInformation", method=self.GetServerInformation
        )
        self.__dbus.register_dbus_method(
            name="GetCapabilities", method=self.GetCapabilities
        )
        self.__dbus.register_dbus_method(
            name="CloseNotification", method=self.CloseNotification
        )
        self.__dbus.register_dbus_method(name="Notify", method=self.Notify)

        self._id = 1
        self._notifications = {}
        self._popups = {}
        self._dnd = False

        self.__load_notifications()

    @GObject.Property
    def notifications(self) -> list:
        return sorted(
            list(self._notifications.values()), key=lambda x: x.id, reverse=True
        )

    @GObject.Property
    def popups(self) -> list:
        return sorted(list(self._popups.values()), key=lambda x: x.id, reverse=True)

    @GObject.Property
    def dnd(self) -> bool:
        return self._dnd

    @dnd.setter
    def dnd(self, value: bool) -> None:
        self._dnd = value
        self.__sync()
        self.emit("toggled_dnd", self._dnd)

    def toggle_dnd(self) -> None:
        self.dnd = not self._dnd

    def set_dnd(self, value: bool) -> None:
        self.dnd = value

    def GetServerInformation(self, *args) -> GLib.Variant:
        return GLib.Variant(
            "(ssss)",
            ("linkfrg's notification daemon", "linkfrg", "1.0", "1.2"),
        )

    def GetCapabilities(self, *args) -> GLib.Variant:
        return GLib.Variant(
            "(as)", (["actions", "body", "icon-static", "persistence"],)
        )

    def CloseNotification(self, invocation, id: int) -> None:
        self.get_notification(id).close()

    def get_notification(self, id: int) -> Notification:
        return self._notifications.get(id, None)

    def Notify(
        self,
        invocation,
        app_name: str,
        replaces_id: int,
        app_icon: str,
        summary: str,
        body: str,
        actions: list,
        hints: dict,
        timeout: int,
    ) -> GLib.Variant:
        acts = []
        icon = None

        if replaces_id != 0:
            id = replaces_id
        else:
            id = self._id = self._id + 1

        for i in range(0, len(actions), 2):
            acts.append({"id": str(actions[i]), "label": str(actions[i + 1])})

        if isinstance(app_icon, str):
            icon = app_icon

        if "image-data" in hints:
            icon = f"{NOTIFICATIONS_IMAGE_DATA}/{id}"
            self.__save_pixbuf(hints["image-data"], icon)

        notification = Notification(
            id=id,
            app_name=app_name,
            icon=icon,
            summary=summary,
            body=body,
            actions=acts,
            urgency=hints.get("urgency", 1),
            timeout=timeout,
            time=datetime.datetime.now().strftime("%H:%M"),
            popup=not self._dnd,
        )

        if len(self.popups) > 3:
            self.popups[-1].dismiss()

        if notification.popup:
            self._popups[notification.id] = notification
            self.emit("new_popup", notification)
            self.notify('popups')

        self.__add_notification(notification)
        self.__sync()
        self.emit("notified", notification)
        self.notify('notifications')

        return GLib.Variant("(u)", (id,))

    def __save_pixbuf(self, px_args, save_path: str) -> None:
        GdkPixbuf.Pixbuf.new_from_bytes(
            width=px_args[0],
            height=px_args[1],
            has_alpha=px_args[3],
            data=GLib.Bytes(px_args[6]),
            colorspace=GdkPixbuf.Colorspace.RGB,
            rowstride=px_args[2],
            bits_per_sample=px_args[4],
        ).savev(save_path, "png")

    def clear_all(self) -> None:
        for notify in self.notifications:
            notify.close()

    def __close_notification(self, notification: Notification) -> None:
        self._notifications.pop(notification.id)
        if notification.popup:
            notification.dismiss()
        self.__sync()

        self.__dbus.emit_signal(
            "NotificationClosed", GLib.Variant("(uu)", (notification.id, 2))
        )

        self.emit("closed", notification)
        self.notify('notifications')

    def __dismiss_popup(self, notification: Notification) -> None:
        if self._popups.get(notification.id, None):
            self._popups.pop(notification.id)
            self.emit("dismissed", notification)
            self.notify('popups')

    def __invoke_action(self, notification: Notification, action: str) -> None:
        self.__dbus.emit_signal(
            "ActionInvoked", GLib.Variant("(us)", (notification.id, action))
        )

    def __sync(self) -> None:
        data = {
            "id": self._id,
            "notifications": [n.json for n in self.notifications],
            "dnd": self._dnd,
        }
        write_json(NOTIFICATIONS_CACHE_FILE, data)

    def __add_notification(self, notification: Notification) -> None:
        notification.connect("closed", lambda x: self.__close_notification(x))
        notification.connect("dismissed", lambda x: self.__dismiss_popup(x))
        notification.connect(
            "action_invoked", lambda x, action: self.__invoke_action(x, action)
        )
        self._notifications[notification.id] = notification

    def __load_notifications(self) -> None:
        try:
            log_file = read_json(
                NOTIFICATIONS_CACHE_FILE, NOTIFICATIONS_EMPTY_CACHE_FILE
            )
            for n in log_file.get("notifications", []):
                notification = Notification(**n, popup=False)
                self.__add_notification(notification)

            self._id = log_file.get("id", 0)
            self._dnd = log_file.get("dnd", False)
        except Exception:
            print("Notification history file is corrupted! Cleaning...")
            write_json(NOTIFICATIONS_CACHE_FILE, NOTIFICATIONS_EMPTY_CACHE_FILE)


notifications = NotificationService()

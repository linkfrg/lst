import json
import os
import threading
import socket
from gi.repository import GObject
from lst.base_service import BaseService
from typing import List

HYPRLAND_INSTANCE_SIGNATURE = os.getenv("HYPRLAND_INSTANCE_SIGNATURE")


class HyprlandService(BaseService):
    __gsignals__ = {
        "workspaces_changed": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
        "kb_layout_changed": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
        "active_window_changed": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def __init__(self):
        super().__init__()
        self.__sync_workspaces()
        self._kb_layout = "English (US)"
        self._active_window = ""

        threading.Thread(target=self.__monitor_socket, daemon=True).start()

    @GObject.Property
    def workspaces(self) -> List[dict]:
        return self._workspaces

    @GObject.Property
    def active_workspace(self) -> dict:
        return self._active_workspace

    @GObject.Property
    def kb_layout(self) -> str:
        return self._kb_layout

    @GObject.Property
    def active_window(self) -> str:
        return self._active_window

    def __monitor_socket(self) -> None:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
            sock.connect(f"/tmp/hypr/{HYPRLAND_INSTANCE_SIGNATURE}/.socket2.sock")
            while True:
                data = sock.recv(1024).decode("utf-8").split("\n")
                if data:
                    for d in data:
                        if (
                            d.startswith("workspace>>")
                            or d.startswith("destroyworkspace>>")
                            or d.startswith("focusedmon>>")
                        ):
                            self.__sync_workspaces()
                        elif d.startswith("activelayout>>"):
                            self._kb_layout = d.split(",")[1].replace("\n", "")
                            self.notify('kb_layout')
                            self.emit("kb_layout_changed")

                        elif d.startswith("activewindow>>"):
                            self._active_window = d.replace("activewindow>>", "").split(
                                ","
                            )[1]
                            self.emit("active_window_changed")

    def __sync_workspaces(self) -> None:
        self._workspaces = sorted(
            json.loads(self.send_command("j/workspaces")), key=lambda x: x["id"]
        )
        self._active_workspace = json.loads(self.send_command("j/activeworkspace"))
        self.emit("workspaces_changed")
        self.notify('workspaces')
        self.notify('active-workspace')

    def send_command(self, cmd: str) -> None:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
            sock.connect(f"/tmp/hypr/{HYPRLAND_INSTANCE_SIGNATURE}/.socket.sock")
            sock.send(cmd.encode())
            resp = sock.recv(4096).decode()
            return resp

    def switch_kb_layout(self) -> None:
        for kb in json.loads(self.send_command("j/devices"))["keyboards"]:
            self.send_command(f"switchxkblayout {kb['name']} next")

    def switch_to_workspace(self, workspace_id: int) -> None:
        self.send_command(f"dispatch workspace {workspace_id}")


hyprland = HyprlandService()

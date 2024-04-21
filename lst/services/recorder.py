from gi.repository import GObject, Gst, GLib
from lst.base_service import BaseService
from lst.dbus import DbusClient
from lst.app import app
import datetime

PIPELINE_TEMPLATE = """
    pipewiresrc path={node_id} do-timestamp=true keepalive-time=1000 resend-last=true !
    videoconvert chroma-mode=none dither=none matrix-mode=output-only n-threads={n_threads} !
    queue !
    x264enc bitrate={bitrate} threads={n_threads} !
    queue !
    h264parse !
    mp4mux fragment-duration=500 fragment-mode=first-moov-then-finalise name=mux !
    filesink location={filename}
    """

AUDIO_PIPELINE = """
    autoaudiosrc !
    queue !
    audioconvert !
    audioresample !
    opusenc !
    mux.
"""


class RecorderService(BaseService):
    __gsignals__ = {
        "recording_started": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
        "recording_stopped": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def __init__(self):
        super().__init__()
        Gst.init(None)
        self.__dbus = DbusClient(
            name="org.freedesktop.portal.Desktop",
            object_path="/org/freedesktop/portal/desktop",
            interface_name="org.freedesktop.portal.ScreenCast",
        )
        self._session_token_counter = 0
        self._request_token_counter = 0
        self._state = False
        self._pipeline_description = ""
        self.__pipeline = None
        self._sender_name = (
            self.__dbus.connection.get_unique_name().replace(".", "_").replace(":", "")
        )
        app.connect('quit', lambda x: self.stop_recording())

    @GObject.Property
    def state(self) -> bool:
        return self._state

    def start_recording(
        self, filename: str = None, bitrate: int = 8000, record_audio: bool = False
    ) -> None:
        n_threads = min(max(1, GLib.get_num_processors()), 64)
        if filename is None:
            filename = (
                GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_VIDEOS)
                + "/"
                + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                + ".mp4"
            )
        self._pipeline_description = PIPELINE_TEMPLATE
        self._pipeline_description = (
            PIPELINE_TEMPLATE.replace("{n_threads}", str(n_threads))
            .replace("{filename}", filename)
            .replace("{bitrate}", str(bitrate))
        )
        if record_audio:
            self._pipeline_description += AUDIO_PIPELINE
        self.__create_session()

    def __request_response(self, callback: callable) -> str:
        self._request_token_counter += 1
        request_token = f"u{self._request_token_counter}"
        request_path = f"/org/freedesktop/portal/desktop/request/{self._sender_name}/{request_token}"
        self.__dbus.signal_subscribe(
            signal_name="Response",
            object_path=request_path,
            interface_name="org.freedesktop.portal.Request",
            callback=callback,
        )
        return request_token

    def __create_session(self) -> None:
        request_token = self.__request_response(self.__on_create_session_response)
        self._session_token_counter += 1
        session_token = f"u{self._session_token_counter}"
        self.__dbus.call_sync(
            method_name="CreateSession",
            parameters=GLib.Variant(
                "(a{sv})",
                (
                    {
                        "session_handle_token": GLib.Variant("s", session_token),
                        "handle_token": GLib.Variant("s", request_token),
                    },
                ),
            ),
        )

    def __on_create_session_response(self, *args):
        response = args[5]
        response_code = response[0]
        self._session = response[1]["session_handle"]

        if response_code != 0:
            self.stop_recording()
            return

        request_token = self.__request_response(self.__on_select_sources_response)

        self.__dbus.call_sync(
            method_name="SelectSources",
            parameters=GLib.Variant(
                "(oa{sv})",
                (
                    self._session,
                    {
                        "handle_token": GLib.Variant("s", request_token),
                        "multiple": GLib.Variant("b", False),
                        "types": GLib.Variant("u", 1 | 2),
                    },
                ),
            ),
        )

    def __on_select_sources_response(self, *args) -> None:
        response_code = args[5][0]

        if response_code != 0:
            self.stop_recording()
            return

        request_token = self.__request_response(self.__on_start_response)
        self.__dbus.call_sync(
            method_name="Start",
            parameters=GLib.Variant(
                "(osa{sv})",
                (
                    self._session,
                    "",
                    {
                        "handle_token": GLib.Variant("s", request_token),
                    },
                ),
            ),
        )

    def __on_start_response(self, *args):
        results = args[5][1]
        response_code = args[5][0]
        if response_code != 0:
            self.stop_recording()
            return

        for node_id, stream_properties in results["streams"]:
            self.__play_pipewire_stream(node_id)

    def __play_pipewire_stream(self, node_id: int) -> None:
        self._pipeline_description = self._pipeline_description.replace('{node_id}', str(node_id))
        self.__pipeline = Gst.parse_launch(self._pipeline_description)
        self.__pipeline.set_state(Gst.State.PLAYING)
        self.__pipeline.get_bus().connect("message", self.__on_gst_message)
        self._state = True
        self.notify("state")
        self.emit("recording_started")

    def __on_gst_message(self, bus, message):
        if message.type == Gst.MessageType.EOS or message.type == Gst.MessageType.ERROR:
            self.stop_recording()

    def stop_recording(self) -> None:
        if self.__pipeline:
            self.__pipeline.send_event(Gst.Event.new_eos())
            self.__pipeline = None
            self._pipeline_description = ""
            self._state = False
            self.notify("state")
            self.emit("recording_stopped")


recorder = RecorderService()

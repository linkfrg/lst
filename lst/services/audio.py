import threading
import pulsectl
from gi.repository import GObject
from lst.services.base_service import BaseService

PULSE = pulsectl.Pulse("lst-audio-service", threading_lock=True)
PULSE_MONITOR = pulsectl.Pulse("lst-audio-service-monitor", threading_lock=True)


class Sink(BaseService):
    def __init__(self, sink):
        super().__init__()
        self._sink = sink

    @GObject.Property
    def sink(self) -> pulsectl.PulseSinkInfo:
        return self._sink

    @GObject.Property
    def description(self) -> str:
        return self.sink.description

    @GObject.Property
    def index(self) -> int:
        return self.sink.index

    @GObject.Property
    def is_muted(self) -> bool:
        return PULSE.get_sink_by_name(self.name).mute
    
    @GObject.Property
    def is_default(self) -> bool:
        return PULSE.server_info().default_sink_name == self.name

    @GObject.Property
    def name(self) -> str:
        return self.sink.name

    @GObject.Property
    def volume(self) -> int:
        if self.is_muted:
            return 0
        else:
            return round(PULSE.get_sink_by_name(self.name).volume.value_flat * 100)

    def set_volume(self, value: int) -> None:
        PULSE.volume_set_all_chans(self.sink, value / 100)

    def mute(self) -> None:
        PULSE.mute(self.sink, True)

    def unmute(self) -> None:
        PULSE.mute(self.sink, False)

    def toggle_mute(self) -> None:
        if self.is_muted:
            self.unmute()
        else:
            self.mute()

    @GObject.Property
    def icon_name(self) -> str:
        template = "audio-volume-{}-symbolic"
        if self.is_muted:
            return template.format("muted")
        elif self.volume > 67:
            return template.format("high")
        elif self.volume > 33:
            return template.format("medium")
        else:
            return template.format("low")


class Source(BaseService):
    def __init__(self, source):
        super().__init__()
        self._source = source

    @GObject.Property
    def source(self) -> pulsectl.PulseSinkInfo:
        return self._source

    @GObject.Property
    def description(self) -> str:
        return self.source.description

    @GObject.Property
    def index(self) -> int:
        return self.source.index

    @GObject.Property
    def is_muted(self) -> bool:
        return PULSE.get_source_by_name(self.name).mute
    
    @GObject.Property
    def is_default(self) -> bool:
        return PULSE.server_info().default_source_name == self.name

    @GObject.Property
    def name(self) -> str:
        return self.source.name

    @GObject.Property
    def volume(self) -> int:
        if self.is_muted:
            return 0
        else:
            return round(PULSE.get_source_by_name(self.name).volume.value_flat * 100)

    def set_volume(self, value: int) -> None:
        PULSE.volume_set_all_chans(self.source, value / 100)

    def mute(self) -> None:
        PULSE.mute(self.source, True)

    def unmute(self) -> None:
        PULSE.mute(self.source, False)

    def toggle_mute(self) -> None:
        if self.is_muted:
            self.unmute()
        else:
            self.mute()

    @GObject.Property
    def icon_name(self) -> str:
        template = "microphone-sensitivity-{}-symbolic"
        if self.is_muted:
            return template.format("muted")
        elif self.volume > 67:
            return template.format("high")
        elif self.volume > 33:
            return template.format("medium")
        else:
            return template.format("low")

class DefaultSink(Sink):
    def __init__(self):
        self.update()
        super().__init__(sink=self.sink)

    def update(self) -> None:
        self._sink = PULSE.get_sink_by_name(PULSE.server_info().default_sink_name)

class DefaultSource(Source):
    def __init__(self):
        self.update()
        super().__init__(source=self.source)

    def update(self) -> None:
        self._source = PULSE.get_source_by_name(PULSE.server_info().default_source_name)
        self.notify_all()


class AudioService(BaseService):
    __gsignals__ = {
        "sink_changed": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
        "source_changed": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
        "devices_changed": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def __init__(self):
        super().__init__()
        self._sinks = []
        self._sources = []
        self._default_sink = DefaultSink()
        self._default_source = DefaultSource()
        self.__update_sink_list()
        self.__update_sources_list()

        threading.Thread(target=self.__main, daemon=True).start()

    def __main(self):
        PULSE_MONITOR.event_mask_set("all")
        PULSE_MONITOR.event_callback_set(self.__monitor)
        PULSE_MONITOR.event_listen()

    def __monitor(self, event) -> None:
        if event.t == "change":
            if event.facility == "sink":
                self.default_sink.notify_all()
                self.emit("sink_changed")
            elif event.facility == "source":
                self.default_source.notify_all()
                self.emit("source_changed")
            elif event.facility == "server":
                self.default_sink.update()
                self.default_source.update()
                self.notify_all()
                self.emit("devices_changed")
            elif event.facility == "card":
                self.__update_sink_list()
                self.__update_sources_list()
                self.notify_all()
                self.emit("devices_changed")
            

    @GObject.Property
    def sinks(self) -> list:
        return self._sinks

    @GObject.Property
    def sources(self) -> list:
        return self._sources

    @GObject.Property
    def default_sink(self) -> DefaultSink:
        return self._default_sink

    @default_sink.setter
    def default_sink(self, value: Sink) -> None:
        PULSE.sink_default_set(value.sink)

    @GObject.Property
    def default_source(self) -> DefaultSource:
        return self._default_source

    @default_source.setter
    def default_source(self, value: Source) -> None:
        PULSE.source_default_set(value.source)

    def __update_sink_list(self) -> None:
        self._sinks = []
        for i in PULSE.sink_list():
            obj = Sink(i)
            self._sinks.append(obj)

    def __update_sources_list(self) -> None:
        self._sources = []
        for i in PULSE.source_list():
            obj = Source(i)
            self._sources.append(obj)


audio = AudioService()

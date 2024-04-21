import threading
import pulsectl
from gi.repository import GObject
from lst.base_service import BaseService
from typing import List

PULSE = pulsectl.Pulse("lst-audio-service", threading_lock=True)
PULSE_MONITOR = pulsectl.Pulse("lst-audio-service-monitor", threading_lock=True)


class Device(BaseService):
    def __init__(self, device):
        super().__init__()
        self._device = device

    @GObject.Property
    def device(self):
        pass

    @GObject.Property
    def name(self) -> str:
        return self.device.name

    @GObject.Property
    def description(self) -> str:
        return self.device.description

    @GObject.Property
    def index(self) -> int:
        return self.device.index

    @GObject.Property
    def is_muted(self) -> bool:
        return self.device.mute

    @GObject.Property
    def is_default(self) -> bool:
        pass

    @GObject.Property
    def volume(self) -> int:
        if self.is_muted:
            return 0
        else:
            return round(self.device.volume.value_flat * 100)

    @GObject.Property
    def icon_name(self) -> str:
        if self.is_muted:
            return "muted"
        elif self.volume > 67:
            return "high"
        elif self.volume > 33:
            return "medium"
        else:
            return "low"

    def set_volume(self, value: int) -> None:
        PULSE.volume_set_all_chans(self._device, value / 100)

    def mute(self) -> None:
        PULSE.mute(self._device, True)

    def unmute(self) -> None:
        PULSE.mute(self._device, False)

    def toggle_mute(self) -> None:
        if self.is_muted:
            self.unmute()
        else:
            self.mute()


class Sink(Device):
    def __init__(self, sink: pulsectl.PulseSinkInfo):
        super().__init__(device=sink)

    @GObject.Property
    def device(self) -> pulsectl.PulseSinkInfo:
        return PULSE.get_sink_by_name(self._device.name)

    @GObject.Property
    def is_default(self) -> bool:
        return PULSE.server_info().default_sink_name == self.name

    @GObject.Property
    def icon_name(self) -> str:
        template = "audio-volume-{}-symbolic"
        return template.format(super().icon_name)


class Source(Device):
    def __init__(self, source: pulsectl.PulseSourceInfo):
        super().__init__(device=source)

    @GObject.Property
    def device(self) -> pulsectl.PulseSourceInfo:
        return PULSE.get_source_by_name(self._device.name)

    @GObject.Property
    def is_default(self) -> bool:
        return PULSE.server_info().default_source_name == self.name

    @GObject.Property
    def icon_name(self) -> str:
        template = "microphone-sensitivity-{}-symbolic"
        return template.format(super().icon_name)


class DefaultSink(Sink):
    def __init__(self):
        self.update()
        super().__init__(sink=self._device)

    def update(self) -> None:
        self._device = PULSE.get_sink_by_name(PULSE.server_info().default_sink_name)
        self.notify_all()


class DefaultSource(Source):
    def __init__(self):
        self.update()
        super().__init__(source=self._device)

    def update(self) -> None:
        self._device = PULSE.get_source_by_name(PULSE.server_info().default_source_name)
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
    def sinks(self) -> List[Sink]:
        return self._sinks

    @GObject.Property
    def sources(self) -> List[Source]:
        return self._sources

    @GObject.Property
    def default_sink(self) -> DefaultSink:
        return self._default_sink

    def set_default_sink(self, value: Sink) -> None:
        PULSE.sink_default_set(value.device)

    @GObject.Property
    def default_source(self) -> DefaultSource:
        return self._default_source

    def set_default_source(self, value: Source) -> None:
        PULSE.source_default_set(value.device)

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

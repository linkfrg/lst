from gi.repository import GObject, NM
from lst.services.base_service import BaseService

STATE = {
    NM.DeviceState.UNKNOWN: "unknown",
    NM.DeviceState.UNMANAGED: "unmanaged",
    NM.DeviceState.ACTIVATED: "activated",
    NM.DeviceState.DEACTIVATING: "deactivating",
    NM.DeviceState.FAILED: "failed",
    NM.DeviceState.UNAVAILABLE: "unavailable",
    NM.DeviceState.DISCONNECTED: "disconnected",
    NM.DeviceState.PREPARE: "prepare",
    NM.DeviceState.CONFIG: "config",
    NM.DeviceState.NEED_AUTH: "need_auth",
    NM.DeviceState.IP_CONFIG: "ip_config",
    NM.DeviceState.IP_CHECK: "ip_check",
    NM.DeviceState.SECONDARIES: "secondaries",
}


class WifiAccessPoint(BaseService):
    def __init__(self, point: NM.AccessPoint):
        self._point = point
        super().__init__()
        self._point.connect('notify::strength', lambda *args: (self.notify('strength'), self.notify('icon-name')))

    @GObject.Property
    def bandwidth(self) -> int:
        return self._point.props.bandwidth

    @GObject.Property
    def bssid(self) -> str:
        return self._point.props.bssid

    @GObject.Property
    def frequency(self) -> int:
        return self._point.props.frequency

    @GObject.Property
    def hw_address(self) -> str:
        return self._point.props.hw_address

    @GObject.Property
    def last_seen(self) -> int:
        return self._point.props.last_seen

    @GObject.Property
    def max_bitrate(self) -> int:
        return self._point.props.max_bitrate

    @GObject.Property
    def ssid(self) -> str:
        if self._point.props.ssid:
            return NM.utils_ssid_to_utf8(self._point.props.ssid.get_data())
        else:
            return ""

    @GObject.Property
    def strength(self) -> int:
        return self._point.props.strength
    
    @GObject.Property
    def icon_name(self) -> str:
        if self.strength > 80:
            return 'network-wireless-signal-excellent-symbolic'
        elif self.strength > 60:
            return 'network-wireless-signal-good-symbolic'
        elif self.strength > 40:
            return 'network-wireless-signal-ok-symbolic'
        elif self.strength > 20:
            return 'network-wireless-signal-weak-symbolic'
        elif self.strength > 0:
            return 'network-wireless-signal-none-symbolic'
        

class ActiveAccessPoint(WifiAccessPoint):
    def __init__(self, client: NM.Client, device: NM.DeviceType.WIFI):
        self.__client = client
        self.__device = device
        self.update()
        super().__init__(self._point)

    def update(self) -> None:
        ap = self.__device.get_active_access_point()
        if ap:
            self._point = ap
        else:
            self._point = NM.AccessPoint()
        self.notify_all()

    @GObject.Property
    def icon_name(self) -> str:
        template = 'network-wireless-signal-{}-symbolic'
        ac = self.__client.get_activating_connection()
        if ac:
            if ac.get_state() == NM.ActiveConnectionState.ACTIVATING:
                return 'network-wireless-acquiring-symbolic'


        if self.strength > 80:
            return template.format('excellent')
        elif self.strength > 60:
            return template.format('good')
        elif self.strength > 40:
            return template.format('ok')
        elif self.strength > 20:
            return template.format('weak')
        elif self.strength > 0:
            return template.format('none')
        
        return 'network-wireless-offline-symbolic'

# TODO
class Ethernet(BaseService):
    def __init__(self):
        super().__init__()


class Wifi(BaseService):
    def __init__(self, client: NM.Client, device: NM.DeviceType.WIFI):
        super().__init__()
        self.__client = client
        self.__device = device
        self.__client.connect(
            "notify::wireless-enabled", lambda *args: self.notify_all()
        )
        self.__client.connect('notify::activating-connection', lambda *args: self.ap.notify('icon-name'))
        if self.__device:
            self._ap = ActiveAccessPoint(self.__client, self.__device)
            self.__device.connect(
                "access-point-added", lambda *args: self.notify("access_points")
            )
            self.__device.connect(
                "access-point-removed", lambda *args: self.notify("access_points")
            )
            self.__device.connect(
                "notify::active-access-point",
                lambda *args: self.__update_ap(),
            )
            self.__update_ap()

    @GObject.Property
    def access_points(self) -> list:
        if self.__device:
            return [WifiAccessPoint(i) for i in self.__device.get_access_points()]
        else:
            return []

    @GObject.Property
    def ap(self):
        return self._ap

    @GObject.Property
    def state(self) -> str:
        return STATE.get(self.__device.get_state(), None)
    
    @GObject.Property
    def enabled(self) -> bool:
        return self.__client.wireless_get_enabled()

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self.__client.wireless_set_enabled(value)

    def set_enabled(self, value: bool) -> None:
        self.enabled = value

    def __update_ap(self) -> None:
        self._ap.update()
        self.notify("ap")

    def scan(self) -> None:
        if self.__device and self.state != 'unavailable':
            self.__device.request_scan_async(
                None, lambda x, result: self.__device.request_scan_finish(result)
            )


class NetworkService(BaseService):
    def __init__(self):
        super().__init__()

        self.__client = NM.Client.new(None)
        self.__sync()

    @GObject.Property
    def wifi(self) -> Wifi:
        return self._wifi

    def __get_device(self, device_type: NM.DeviceType):
        for d in self.__client.get_devices():
            if d.get_device_type() == device_type:
                return d

    def __sync(self) -> None:
        wifi_device = self.__get_device(device_type=NM.DeviceType.WIFI)
        self._wifi = Wifi(
            client=self.__client,
            device=wifi_device,
        )


network = NetworkService()

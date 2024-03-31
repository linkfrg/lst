from gi.repository import GObject, GLib
from datetime import datetime
from lst.services.base_service import BaseService


class TimeService(BaseService):
    def __init__(self):
        super().__init__()
        self._time = int(datetime.now().timestamp())
        self.__main()

    def __main(self) -> None:
        self._time = int(datetime.now().timestamp())
        self.notify('time')
        GLib.timeout_add_seconds(1, self.__main)

    def get_time_format(self, time:int, time_format: str) -> None:
        return datetime.fromtimestamp(time).strftime(time_format)
    
    @GObject.Property
    def time(self) -> int:
        return self._time


time = TimeService()

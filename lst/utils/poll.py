from lst.base_service import BaseService
from gi.repository import GLib, GObject


class Poll(BaseService):
    __gsignals__ = {
        "changed": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
    }
    def __init__(self, timeout: int, callback: callable, *args):
        super().__init__()
        self._output = None
        self._timeout = timeout
        self._callback = callback
        self._args = args
        self.__main()

    @GObject.Property
    def output(self) -> str:
        return self._output

    def __main(self) -> None:        
        self._output = self._callback(*self._args)
        self.emit("changed")
        self.notify('output')
        GLib.timeout_add_seconds(self._timeout, self.__main)

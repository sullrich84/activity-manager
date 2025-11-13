from textual.message import Message


class BusyMessage(Message):
    bubble = True

    def __init__(self, busy: bool):
        super().__init__()
        self.busy = busy

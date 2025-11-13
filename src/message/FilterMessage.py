from textual.message import Message


class FilterMessage(Message):
    def __init__(self, start_date: str, end_date: str | None = None):
        super().__init__()
        self.start_date = start_date
        self.end_date = end_date

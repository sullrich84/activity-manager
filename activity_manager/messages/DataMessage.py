from textual.message import Message
from activity_manager.models import ActivityModel


class DataMessage(Message):
    bubble = True

    def __init__(self, data: list[ActivityModel]):
        super().__init__()
        self.data = data

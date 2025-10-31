from textual.message import Message

from lib.models import ActivityItem


class ActivitiesMessage(Message):
    def __init__(self, value: list[ActivityItem]):
        self.value = value
        super().__init__()

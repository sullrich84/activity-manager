from datetime import datetime
from dateutil.relativedelta import relativedelta
from textual.app import ComposeResult
from textual.validation import ValidationResult, Validator
from textual.widgets import Input
from textual.events import Key


class DateValidator(Validator):
    def validate(self, value: str) -> ValidationResult:
        try:
            DateInput.format_date(value)
            return self.success()
        except ValueError:
            return self.failure()


class DateInput(Input):
    BINDINGS = [
        ("ctrl+a", "update_value(-1)", "increase"),
        ("ctrl+x", "update_value(+1)", "decrease"),
        ("ctrl+t", "set_today()", "today"),
    ]

    def compose(self) -> ComposeResult:
        self.validators.append(DateValidator("Invalid Date"))
        self.validate_on.add("blur")
        self.validate_on.add("submitted")
        self.validate_on.add("changed")
        return super().compose()

    def on_key(self, event: Key) -> None:
        if not event.key.isdigit() and not event.key == "minus":
            event.prevent_default()

    def action_update_value(self, value: int):
        current_value = datetime.strptime(self.value, "%Y-%m-%d")
        if self.cursor_position <= 4:
            delta = relativedelta(years=value)
        elif self.cursor_position <= 7:
            delta = relativedelta(months=value)
        else:
            delta = relativedelta(days=value)

        next_value = current_value - delta
        self.value = DateInput.format_date(str(next_value))

    def action_set_today(self):
        self.value = DateInput.format_date(str(datetime.now()))

    @staticmethod
    def format_date(input: str):
        input = input.split(" ")[0]
        date = datetime.strptime(input, "%Y-%m-%d")
        return f"{date.year}-{date.month:0>2}-{date.day:0>2}"

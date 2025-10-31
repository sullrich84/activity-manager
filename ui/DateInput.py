from datetime import datetime, timedelta
from textual import events
from textual.validation import ValidationResult, Validator
from textual.widgets import Input


class DateValidator(Validator):
    def validate(self, value: str) -> ValidationResult:
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            return self.failure()
        finally:
            return self.success() if len(value) == 10 else self.failure()


class DateInput(Input):
    DEFAULT_CSS = """
        DateInput {
            width: 12;
        }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            validators=[DateValidator("Invalid Date")],
            validate_on=["blur", "submitted", "changed"],
            **kwargs,
        )

    def update_value(self, delta_days: int):
        current_value = datetime.strptime(self.value, "%Y-%m-%d")
        self.value = str(current_value - timedelta(days=delta_days))

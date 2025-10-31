from datetime import datetime
from textual.validation import ValidationResult, Validator
from textual.widgets import Input


class DateValidator(Validator):
    def validate(self, value: str) -> ValidationResult:
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return self.success()
        except ValueError:
            return self.failure()


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

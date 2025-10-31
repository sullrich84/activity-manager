from textual.widgets import Label as TextualLabel


class Label(TextualLabel):
    DEFAULT_CSS = """
        Label {
            margin-left: 1;
            margin-right: 1;
        }
    """

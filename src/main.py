from textual.app import App, ComposeResult
from textual.widgets import Header, Footer


class HarbApp(App):

    BINDINGS = [
        ("k", "kill_port", "Kill")
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Footer()

    def action_kill_port(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark


if __name__ == "__main__":
    app = HarbApp()
    app.run()

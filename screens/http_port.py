from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal, Center
from textual.widgets import Button, Label, Header, Footer
from textual.screen import Screen
from screens.progress import ProgressScreen  

class HTTPPortScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            yield Vertical(
                Label("🌐 Enable HTTP access port?"),
                Horizontal(
                    Button("Yes", id="yes", classes="primary-btn"),
                    Button("No", id="no", classes="secondary-btn"),
                ),
                id="form-container"
            )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        self.app.push_screen(ProgressScreen())

from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Header, Footer, Label, Button
from screens.license import LicenseScreen

class WelcomeScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Label("Welcome to the FDSA Installer!"),
            Button("Start Installation", id="start", classes="primary-btn"),
            id="center"
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.app.push_screen(LicenseScreen())
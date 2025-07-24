from textual.app import App, ComposeResult
from textual.containers import Vertical, Center
from textual.widgets import Button, Label, Header, Footer
from textual.screen import Screen

class FinalScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            yield Vertical(
                Label("🎉 Installation Complete!"),
                Label("✅ FDSA has been installed successfully."),
                Label("Please save your credentials securely."),
                Button("Exit", id="exit", classes="primary-btn"),
                id="form-container"
            )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        self.app.exit("Installation finished")


from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal, Center
from textual.widgets import Button, Label, Header, Footer
from textual.screen import Screen

class UbuntuInfoScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            yield Vertical(
                Label("FDSA will install the following packages:", id="title"),
                Vertical(
                    Label("• apt-transport-https"),
                    Label("• ca-certificates"),
                    Label("• curl"),
                    Label("• gnupg"),
                    Label("• lsb-release"),
                    Label("• neofetch"),
                    Label("• postgresql-client"),
                    Label("• telnet"),
                    Button("Back", id="back", classes="primary-btn"),
                    id="package-list"
                ),
                id="form-container"
            )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        self.app.pop_screen()

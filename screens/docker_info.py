from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal, Center
from textual.widgets import Button, Label, Header, Footer
from textual.screen import Screen


class DockerInfoScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            yield Vertical(
                Label("The following will be installed:" , id="title"),
                Vertical(
                    Label("• Docker Engine"),
                    Label("• docker-ce"),
                    Label("• docker-ce-cli"),
                    Label("• containerd.io"),
                    Label("• docker-compose-plugin"),
                    Label("• jq"),
                    Button("Back", id="back", classes="primary-btn"),
                    id="package-list"
                ),
                id="form-container"
            )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        self.app.pop_screen()

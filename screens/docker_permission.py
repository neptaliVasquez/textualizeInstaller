from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal, Center
from textual.widgets import Button, Label, Header, Footer
from textual.screen import Screen
from screens.postgres_usage import PostgresUsageScreen
from screens.docker_info import DockerInfoScreen


class DockerPermissionScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            yield Vertical(
                Label("⚠️ Docker is required for this installer."),
                Label("Allow FDSA to install Docker and required packages?"),
                Horizontal(
                    Button("Yes", id="yes", classes="primary-btn"),
                    Button("No", id="no", classes="secondary-btn"),
                    Button("More Info", id="info", classes="info-btn"),
                ),
                id="form-container"
            )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "yes":
            self.app.push_screen(PostgresUsageScreen())
        elif event.button.id == "no":
            self.app.exit("User declined Docker installation")
        elif event.button.id == "info":
            self.app.push_screen(DockerInfoScreen())

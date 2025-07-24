from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal, Center
from textual.widgets import Button, Label, Header, Footer
from textual.screen import Screen
from screens.docker_permission import DockerPermissionScreen
from screens.ubuntu_info import UbuntuInfoScreen


class UbuntuPermissionScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            yield Vertical(
                Label("⚠️ This installer will update your OS and install software."),
                Label("Do you want to continue?"),
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
            self.app.push_screen(DockerPermissionScreen())
        elif event.button.id == "no":
            self.app.exit("User declined system update")
        elif event.button.id == "info":
            self.app.push_screen(UbuntuInfoScreen())

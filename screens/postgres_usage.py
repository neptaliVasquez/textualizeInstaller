from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal, Center
from textual.widgets import Button, Label, Header, Footer
from textual.screen import Screen
from screens.database_credentials import DatabaseCredentialsScreen
from screens.proxy_setup import ProxySetupScreen


class PostgresUsageScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            yield Vertical(
                Label("Do you want to use an external PostgreSQL database?"),
                Horizontal(
                    Button("Yes", id="yes", classes="primary-btn"),
                    Button("No", id="no", classes="secondary-btn"),
                ),
                Label("If you choose 'No', a local PostgreSQL database will be created."),
                id="form-container"
            )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "yes":
            self.app.push_screen(DatabaseCredentialsScreen())
        else:
            self.app.push_screen(ProxySetupScreen())

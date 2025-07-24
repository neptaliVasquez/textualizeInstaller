from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal, Center
from textual.widgets import Button, Label, Header, Footer
from textual.screen import Screen
from textual.widgets import Input
from screens.proxy_setup import ProxySetupScreen

class DatabaseCredentialsScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            yield Vertical(
                Label("🔐 Enter external PostgreSQL credentials:", id="form-title"),
                Horizontal(
                    Vertical(
                        Label("📍 Hostname:"),
                        Input(placeholder="e.g. db.example.com", id="PGHOST"),

                        Label("🗄️ Database name:"),
                        Input(placeholder="Database", id="PGDATABASE"),

                        Label("👤 Username:"),
                        Input(placeholder="Username", id="PGUSER"),

                        id="column-left"
                    ),
                    Vertical(
                        Label("🔒 Password:"),
                        Input(password=True, placeholder="Password", id="PGPASSWORD"),

                        Label("🗃️ Keycloak DB name:"),
                        Input(placeholder="Keycloak DB", id="FDSA_KEYCLOAK_DB"),

                        Label("🔢 Port:"),
                        Input(placeholder="5432", id="PGPORT"),

                        id="column-right"
                    ),
                    id="form-columns"
                ),
                Label("", id="error-label"), 
                Horizontal(
                    Button("Next", id="next", classes="primary-btn"),
                    Button("Back", id="back", classes="secondary-btn"),
                ),
                id="form-container"
            )
        yield Footer()

    def on_mount(self):
        self.host = self.query_one("#PGHOST", Input)
        self.db = self.query_one("#PGDATABASE", Input)
        self.user = self.query_one("#PGUSER", Input)
        self.pwd = self.query_one("#PGPASSWORD", Input)
        self.port = self.query_one("#PGPORT", Input)
        self.error_label = self.query_one("#error-label", Label)

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "next":
            # Validación simple
            if not all([
                self.host.value.strip(),
                self.db.value.strip(),
                self.user.value.strip(),
                self.pwd.value.strip(),
                self.port.value.strip().isdigit()
            ]):
                self.error_label.update("❌ Please fill in all fields correctly.")
                return

            # if everything is valid, you can save the values
            self.app.push_screen(ProxySetupScreen())

        elif event.button.id == "back":
            self.app.pop_screen()

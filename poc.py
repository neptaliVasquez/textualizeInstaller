from textual.app import App, ComposeResult
from textual.containers import Vertical, VerticalScroll, Horizontal, Center
from textual.widgets import (
    Header, Footer, Label, Input, Button, Static, RadioButton, Static, RadioSet, Select, LoadingIndicator
)
from textual.screen import Screen
from textual.reactive import reactive
from rich.spinner import Spinner
from textual.app import RenderableType

#  Spinner class to show loading animation
class SpinnerWidget(Static):
    def __init__(self, style: str = "dots8Bit", **kwargs) -> None:
        super().__init__(**kwargs)
        self._spinner = Spinner(style)
        self._renderable: RenderableType = self._spinner

    def on_mount(self) -> None:
        self.set_interval(1 / 20, self._tick)

    def _tick(self) -> None:
        self._spinner.update()
        self.update(self._spinner)

######### SCREENS #########

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


class LicenseScreen(Screen):
    def compose(self):
        with open("LICENSE", "r") as f:
            license_text = f.read()

        yield Vertical(
            Label("📜 License Agreement", id="title"),
            VerticalScroll(
                Static(license_text, id="license-box", markup=True),
                id="license-scroll"
            ),
            Label("By accepting, declining, or using the software, you confirm that you have read and understood the terms of this agreement and agree to follow them.", id="license-note"),
            Horizontal(
                Button("Accept", id="accept", classes="primary-btn"),
                Button("Decline", id="decline", classes="secondary-btn"),
                id="license-buttons"
            ),
            id="license-layout"
        )
        self.license_text = license_text

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "accept":
            self.app.push_screen(FQDNScreen())  # Go to next step
        elif event.button.id == "decline":
            self.app.exit("License declined")

class FQDNScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            yield Vertical(
                Label("🌐 FQDN Setup", id="title"),
                Label("Please enter your Fully Qualified Domain Name (FQDN) below:"),
                Input(placeholder="example.domain.com", id="fqdn-input"),
                Horizontal(
                    Button("Next", id="next", classes="primary-btn"),
                    Button("Back", id="back", classes="secondary-btn")
                ),
                id="form-container"
            )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "next":
            self.app.push_screen(CertCheckScreen())
        elif event.button.id == "back":
            self.app.pop_screen()


class CertCheckScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            yield Vertical(
                Label("🔐 Checking required certificate files..."),
                Label("🗝️  private_keyfile.key"),
                Label("📄 fullchain_certfile.crt"),
                Label("📁 Make sure these files are present in ssl-certs/"),
            Horizontal(
                Button("Next", id="next", classes="primary-btn"),
                Button("Back", id="back", classes="secondary-btn")
            ),
            id="form-container"
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "next":
            self.app.push_screen(UbuntuPermissionScreen())
        elif event.button.id == "back":
            self.app.pop_screen()


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


class DatabaseCredentialsScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            yield Vertical(
                Label("🔐 Enter external PostgreSQL credentials:", id="form-title"),
                Horizontal(
                    # Left Column
                    Vertical(
                        Label("📍 Hostname:"),
                        Input(placeholder="e.g. db.example.com", id="PGHOST"),

                        Label("🗄️ Database name:"),
                        Input(placeholder="Database", id="PGDATABASE"),

                        Label("👤 Username:"),
                        Input(placeholder="Username", id="PGUSER"),

                        id="column-left"
                    ),

                    # Right Column
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
                Horizontal(
                    Button("Next", id="next", classes="primary-btn"),
                    Button("Back", id="back", classes="secondary-btn"),
                ),
                id="form-container"
            )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "next":
            self.app.push_screen(ProxySetupScreen())
        elif event.button.id == "back":
            self.app.pop_screen()

class ProxySetupScreen(Screen):
    selected_proxy: reactive[str] = reactive("none")

    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            yield Vertical(
                Label("🌐 Select a proxy type for your environment:"),
                Select(
                    id="proxy-select",
                    options=[
                        ("🚫 None", "none"),
                        ("🌐 HTTP", "http"),
                        ("🔒 HTTPS", "https"),
                    ],
                    value="none"
                ),
                Input(
                    placeholder="http://proxy.example.com:8080",
                    id="proxy-url",
                    classes="proxy-input hidden"
                ),
                Horizontal(
                    Button("Next", id="next", classes="primary-btn"),
                    Button("Back", id="back", classes="secondary-btn"),
                ),
                id="form-container"
            )
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#proxy-select", Select).focus()

    def on_select_changed(self, event: Select.Changed) -> None:
        self.selected_proxy = event.value
        input_field = self.query_one("#proxy-url", Input)
        if self.selected_proxy in ("http", "https"):
            input_field.remove_class("hidden")
        else:
            input_field.add_class("hidden")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "next":
            self.app.push_screen(SubfolderScreen())
        elif event.button.id == "back":
            self.app.pop_screen()


class SubfolderScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()

        with Center():
            yield Vertical(
                Label("📁 Do you want to use a subfolder for FDSA (e.g., https://domain.com/fdsa)?"),
                RadioSet(
                    RadioButton("Yes", id="yes"),
                    RadioButton("No", id="no", value=True),
                    id="subfolder-choice"
                ),
                Input(placeholder="Subfolder name (e.g., fdsa)", id="subfolder-input"),
                Horizontal(
                    Button("Next", id="next", classes="primary-btn"),
                    Button("Back", id="back", classes="secondary-btn"),
                ),
                id="form-container"
            )

        yield Footer()

    def on_mount(self):
        self.set_focus(self.query_one("#no", RadioButton))
        self.subfolder_input = self.query_one("#subfolder-input", Input)
        self.subfolder_input.display = False  # Hide input by default

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        if event.pressed.id == "yes":
            self.subfolder_input.display = True
        else:
            self.subfolder_input.display = False

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "next":
            self.app.push_screen(HTTPPortScreen())
        elif event.button.id == "back":
            self.app.pop_screen()


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



class ProgressScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()

        with Center():
            yield Vertical(
                Horizontal(
                    Label("⏳ Installation in progress...", classes="progress-label"),
                    SpinnerWidget("dots8Bit", id="spinner"),
                    id="progress-line"
                ),
                Static("This may take a few minutes.", classes="hint-text"),
                Button("Simulate Completion", id="finish", classes="primary-btn"),
                id="form-container"
            )

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        self.app.push_screen(FinalScreen())


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



class InstallerApp(App):
    CSS_PATH = "installer.css"

    def on_mount(self) -> None:
        self.push_screen(WelcomeScreen())


if __name__ == "__main__":
    InstallerApp().run()

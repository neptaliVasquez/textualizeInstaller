from textual.app import App, ComposeResult
from textual.containers import Vertical, VerticalScroll, Horizontal
from textual.widgets import (
    Header, Footer, Label, Input, Button, LoadingIndicator, Static, TextArea, Static
)
from textual.screen import Screen
from textual.reactive import reactive
import asyncio


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
                Button("Decline", id="decline", classes="secondary-btn"),
                Button("Accept", id="accept", classes="primary-btn"),
                id="license-buttons"
            ),
            id="license-layout"
        )
        self.license_text = license_text

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "accept":
            self.app.push_screen(InputScreen())  # Go to next step
        elif event.button.id == "decline":
            self.app.exit("License declined")


class InputScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Label("Please enter your FQDN"),
            Input(placeholder="example.com", id="install_path"),
            Button("Next", id="next", classes="primary-btn"),
            id="center"
        )
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#install_path", Input).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "next":
            path = self.query_one("#install_path", Input).value
            self.app.install_path = path
            self.app.push_screen(SslScreen())


class SslScreen(Screen):
    def compose(self):
        yield Vertical(
            VerticalScroll(
                Label("🔒 SSL Certificate Setup", id="title"),
                Label("Please paste the full contents of each certificate including BEGIN/END lines.\n"),
                Label("🔓 Untrusted Certificate:"),
                TextArea(id="untrusted", classes="cert-box"),
                Label("🔗 Intermediate Certificate:"),
                TextArea(id="intermediate", classes="cert-box"),
                Label("✨ Root Certificate:"),
                TextArea(id="root_cert", classes="cert-box"),
                Label("🔐 Private Key:"),
                TextArea(id="private_key", classes="cert-box"),
                id="scroll-section"
            ),
            Horizontal(
                Button("Back", id="back", classes="secondary-btn"),
                Button("Next", id="next", classes="primary-btn"),
                id="button-row"
            )
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "next":
            untrusted = self.query_one("#untrusted", TextArea).text
            intermediate = self.query_one("#intermediate", TextArea).text
            root_cert = self.query_one("#root_cert", TextArea).text
            private_key = self.query_one("#private_key", TextArea).text

            self.app.untrusted_cert = untrusted
            self.app.intermediate_cert = intermediate
            self.app.root_cert = root_cert
            self.app.private_key = private_key

            # You can now handle validation or navigation
            self.app.push_screen(InstallScreen()) 
        elif event.button.id == "back":
            self.app.pop_screen( )  # Go back to the previous screen


class InstallScreen(Screen):
    progress = reactive(0)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Label("Installing...", id="status"),
            LoadingIndicator(id="indicator"),
            Label("", id="done"),
            id="center"
        )
        yield Footer()

    def on_mount(self) -> None:
        # Delay the install logic so screen renders first
        self.call_after_refresh(self.run_install_steps)

    async def run_install_steps(self) -> None:
        status = self.query_one("#status", Label)
        indicator = self.query_one("#indicator", LoadingIndicator)
        done = self.query_one("#done", Label)

        for i in range(5):
            status.update(f"Installing... step {i+1}/5")
            await asyncio.sleep(1)

        status.update("✅ Installation complete!")
        indicator.display = False
        done.update("You can now use the application.")
        ## close
        done.update("Press Ctrl + Q to exit.")
        done.styles.text_style = "bold"
        done.styles.color = "cyan"

class InstallerApp(App):
    CSS_PATH = "installer.css"

    install_path: str = "example.com"
    untrusted_cert: str = ""
    intermediate_cert: str = ""
    root_cert: str = ""
    private_key: str = ""

    def on_mount(self) -> None:
        self.push_screen(WelcomeScreen())


if __name__ == "__main__":
    InstallerApp().run()

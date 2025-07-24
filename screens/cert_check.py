import os
from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import Center, Vertical, Horizontal
from textual.widgets import Header, Footer, Label, Button
from screens.ubuntu_permission import UbuntuPermissionScreen

class CertCheckScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            yield Vertical(
                Label("🔐 Required Certificate Files Check", id="title"),
                Label("The following files are required in the `ssl-certs/` directory:", id="desc"),
                Label("🗝️  private_keyfile.key"),
                Label("📄 fullchain_certfile.crt"),
                Label("", id="cert-error", classes="error-message"), 
                Horizontal(
                    Button("Next", id="next", classes="primary-btn"),
                    Button("Back", id="back", classes="secondary-btn")
                ),
                id="form-container"
            )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "next":
            missing_files = self._check_certificates()
            error_label = self.query_one("#cert-error", Label)

            if missing_files:
                error_label.update(f"❌ Missing files: {', '.join(missing_files)}")
                return

            self.app.push_screen(UbuntuPermissionScreen())

        elif event.button.id == "back":
            self.app.pop_screen()

    def _check_certificates(self):
        required_files = [
            "ssl-certs/private_keyfile.key",
            "ssl-certs/fullchain_certfile.crt"
        ]
        missing = [f for f in required_files if not os.path.isfile(f)]
        return missing
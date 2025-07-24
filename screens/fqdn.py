# screens/fqdn.py

import re
from textual.screen import Screen
from textual.containers import Vertical, Horizontal, Center
from textual.widgets import Header, Footer, Label, Input, Button
from textual.app import ComposeResult
from screens.cert_check import CertCheckScreen


class FQDNScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            yield Vertical(
                Label("🌐 FQDN Setup", id="title"),
                Label("Please enter your Fully Qualified Domain Name (FQDN) below:"),
                Input(placeholder="example.domain.com", id="fqdn-input"),
                Label("", id="fqdn-error", classes="error-message"),  # Error message
                Horizontal(
                    Button("Next", id="next", classes="primary-btn"),
                    Button("Back", id="back", classes="secondary-btn")
                ),
                id="form-container"
            )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "next":
            fqdn_value = self.query_one("#fqdn-input", Input).value.strip()
            error_label = self.query_one("#fqdn-error", Label)

            if not self._is_valid_fqdn(fqdn_value):
                error_label.update("❌ Please enter a valid FQDN (e.g., example.domain.com).")
                return

            # Aquí puedes guardar el valor en InstallerState si ya lo estás usando
            self.app.state.fqdn = fqdn_value

            self.app.push_screen(CertCheckScreen())

        elif event.button.id == "back":
            self.app.pop_screen()

    def _is_valid_fqdn(self, fqdn: str) -> bool:
        return bool(re.match(r"^(?!-)[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", fqdn))

from textual.screen import Screen
from textual.containers import Vertical, Horizontal, VerticalScroll
from textual.widgets import Label, Button, Static
from screens.fqdn import FQDNScreen


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

import os
from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import Center, Vertical, Horizontal, VerticalScroll
from textual.widgets import Header, Footer, Label, Button, TextArea
from screens.ubuntu_permission import UbuntuPermissionScreen

class CertCheckScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            # yield Vertical(
            #     Label("🔐 Required Certificate Files Check", id="title"),
            #     Label("The following files are required in the `ssl-certs/` directory:", id="desc"),
            #     Label("🗝️  private_keyfile.key"),
            #     Label("📄 fullchain_certfile.crt"),
            #     Label("", id="cert-error", classes="error-message"), 
            #     Horizontal(
            #         Button("Next", id="next", classes="primary-btn"),
            #         Button("Back", id="back", classes="secondary-btn")
            #     ),
            #     id="form-container"
            # )
            yield VerticalScroll(
                Label("🔒 SSL Certificate Check", id="title"),
                Label("📝 Please paste the contents of your SSL certificate files below. Including BEGIN/END lines."),
                Horizontal(
                    Vertical(
                        Label("❗ Untrusted Certificate:"),
                        TextArea(),
                    ),
                    Vertical(
                        Label("🔗 Intermediate Certificate:"),
                        TextArea(),
                    ),
                ),
                Horizontal(
                    Vertical(
                        Label("🌳 Root Certificate:"),
                        TextArea(),
                    ),
                    Vertical(
                        Label("🔑 Private Key:"),
                        TextArea(),
                    ),
                ),
                id="ssl-form",
            )
            yield Horizontal(
                Button("Next", id="next", classes="primary-btn"),
                Button("Back", id="back", classes="secondary-btn"),
                id="btn-row"
            )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "next":
            self.app.push_screen(UbuntuPermissionScreen())

        elif event.button.id == "back":
            self.app.pop_screen()
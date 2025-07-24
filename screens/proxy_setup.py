from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal, Center
from textual.widgets import Button, Label, Header, Footer
from textual.screen import Screen
from textual.widgets import Select, Input
from textual.reactive import reactive
from screens.subfolder import SubfolderScreen


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
                Label("", id="error-label", classes="error-label"),  # mensaje de error
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
        error_label = self.query_one("#error-label", Label)
        proxy_url = self.query_one("#proxy-url", Input).value.strip()

        if event.button.id == "next":
            if self.selected_proxy in ("http", "https") and not proxy_url:
                error_label.update("⚠️ Please enter a valid proxy URL.")
                return
            self.app.push_screen(SubfolderScreen())

        elif event.button.id == "back":
            self.app.pop_screen()

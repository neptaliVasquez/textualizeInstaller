from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal, Center
from textual.widgets import Button, Label, Header, Footer
from textual.screen import Screen
from textual.widgets import RadioSet, RadioButton, Input
from screens.http_port import HTTPPortScreen

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
                Label("", id="error-label", classes="error-label"),  # mensaje de error
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
        self.subfolder_input.display = False

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        if event.pressed.id == "yes":
            self.subfolder_input.display = True
        else:
            self.subfolder_input.display = False

    def on_button_pressed(self, event: Button.Pressed):
        error_label = self.query_one("#error-label", Label)
        if event.button.id == "next":
            use_subfolder = self.query_one("#yes", RadioButton).value
            subfolder_value = self.query_one("#subfolder-input", Input).value.strip()
            if use_subfolder and not subfolder_value:
                error_label.update("⚠️ Please enter a subfolder name.")
                return
            self.app.push_screen(HTTPPortScreen())

        elif event.button.id == "back":
            self.app.pop_screen()

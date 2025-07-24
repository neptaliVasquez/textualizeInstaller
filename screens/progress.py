from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal, Center
from textual.widgets import Button, Label, Header, Footer
from textual.screen import Screen
from textual.widgets import Static
from screens.final import FinalScreen  
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

from textual.app import App
from state import InstallerState

# Import screens
from screens.welcome import WelcomeScreen
from screens.license import LicenseScreen
from screens.fqdn import FQDNScreen
from screens.cert_check import CertCheckScreen
from screens.ubuntu_permission import UbuntuPermissionScreen
from screens.ubuntu_info import UbuntuInfoScreen
from screens.docker_permission import DockerPermissionScreen
from screens.docker_info import DockerInfoScreen
from screens.postgres_usage import PostgresUsageScreen
from screens.database_credentials import DatabaseCredentialsScreen
from screens.proxy_setup import ProxySetupScreen
from screens.subfolder import SubfolderScreen
from screens.http_port import HTTPPortScreen
from screens.progress import ProgressScreen
from screens.final import FinalScreen


class InstallerApp(App):
    CSS_PATH = "installer.css"

    def on_mount(self) -> None:
        self.state = InstallerState()
        self.push_screen(WelcomeScreen())


if __name__ == "__main__":
    InstallerApp().run()

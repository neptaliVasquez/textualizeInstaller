# state.py

from dataclasses import dataclass, field
from typing import Optional

@dataclass
class InstallerState:
    fqdn: Optional[str] = None
    proxy_type: Optional[str] = None
    proxy_url: Optional[str] = None
    use_subfolder: Optional[bool] = None
    subfolder_name: Optional[str] = None
    use_external_db: Optional[bool] = None
    PGHOST: Optional[str] = None
    PGDATABASE: Optional[str] = None
    PGUSER: Optional[str] = None
    PGPASSWORD: Optional[str] = None
    PGPORT: Optional[str] = None
    FDSA_KEYCLOAK_DB: Optional[str] = None
    enable_http: Optional[bool] = None

    def to_dict(self) -> dict:
        return self.__dict__

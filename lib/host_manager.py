import os
import json
from typing import Dict, Optional
from app.database import get_database_atlas
from fastapi import HTTPException

from typing import Dict, Optional
from app.database import get_database_atlas

class HostDatabaseManager:
    def __init__(self, hostname: str):
        self.hostname = hostname
        self.host_config = self.load_host_config()

    def load_host_config(self) -> Dict[str, str]:
        with open("./app/hostname.json") as f:
            host_config = json.load(f)
        return host_config

    def get_database_name(self) -> Optional[str]:
        host_config_entry = self.host_config.get(self.hostname)
        if host_config_entry:
            return host_config_entry.get("databasename")
        return None

    def get_collection(self, collection_name: str):
        database_name = self.get_database_name()
        if database_name:
            return get_database_atlas(database_name)[collection_name]
        raise HTTPException(status_code=404, detail="Database not found for the host")

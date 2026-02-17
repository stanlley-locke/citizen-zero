from django.apps import AppConfig
from django.conf import settings
import json
import os
from pathlib import Path

class ConfigStore:
    CONFIG_FILE = settings.BASE_DIR / 'config.json'
    
    DEFAULTS = {
        "network": {
            "auth_service": "http://127.0.0.1:8000/",
            "id_service": "http://127.0.0.1:8001/",
            "verify_service": "http://127.0.0.1:8002/",
            "audit_service": "http://127.0.0.1:8003/",
            "monitor_service": "http://127.0.0.1:8006/"
        },
        "system": {
            "debug_mode": True,
            "maintenance_mode": False,
            "refresh_rate_sec": 5,
            "max_connections": 100,
            "admin_email": "admin@citizen.gov"
        }
    }

    @classmethod
    def load(cls):
        if not cls.CONFIG_FILE.exists():
            cls.save(cls.DEFAULTS)
            return cls.DEFAULTS
            
        try:
            with open(cls.CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            return cls.DEFAULTS

    @classmethod
    def save(cls, data):
        with open(cls.CONFIG_FILE, 'w') as f:
            json.dump(data, f, indent=4)

class ConfigManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.config_manager'

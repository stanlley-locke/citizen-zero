import os

# Backend Service URLs
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://127.0.0.1:8000/api/v1/auth")
ID_SERVICE_URL = os.getenv("ID_SERVICE_URL", "http://127.0.0.1:8001/api/v1")
VERIFY_SERVICE_URL = os.getenv("VERIFY_SERVICE_URL", "http://127.0.0.1:8002/api/v1")
AUDIT_SERVICE_URL = os.getenv("AUDIT_SERVICE_URL", "http://127.0.0.1:8003/api/v1/audit")
MONITOR_SERVICE_URL = os.getenv("MONITOR_SERVICE_URL", "http://127.0.0.1:8006/api/v1/monitor")

# CLI Settings
TOKENS_FILE = os.path.join(os.path.expanduser("~"), ".citizen_zero_cli_token")
APP_NAME = "Citizen-Zero Admin CLI"
VERSION = "1.0.0"

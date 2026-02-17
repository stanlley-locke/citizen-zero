import os

# Base Configuration
API_HOST = "http://127.0.0.1"

# Service Ports
PORTS = {
    "AUTH": 8000,
    "ID": 8001,
    "VERIFY": 8002,
    "AUDIT": 8003,
    "IPRS": 8005,
}

# Service Base URLs
AUTH_SERVICE_URL = f"{API_HOST}:{PORTS['AUTH']}/api/v1"
ID_SERVICE_URL = f"{API_HOST}:{PORTS['ID']}/api/v1"
AUDIT_SERVICE_URL = f"{API_HOST}:{PORTS['AUDIT']}/api/v1"
VERIFY_SERVICE_URL = f"{API_HOST}:{PORTS['VERIFY']}" # Verify service root
IPRS_SERVICE_URL = f"{API_HOST}:{PORTS['IPRS']}/api/v1"

# Specific Endpoints
class Endpoints:
    # Health Checks
    HEALTH_CHECKS = {
        "Auth Service": f"{AUTH_SERVICE_URL}/auth/health/",
        "ID Service": f"{ID_SERVICE_URL}/health/",
        "Verify Service": f"{VERIFY_SERVICE_URL}/api/v1/verify/health/", 
        "Audit Service": f"{AUDIT_SERVICE_URL}/audit/health/",
        # IPRS doesn't have one yet, mock it
    }

    # Virtual Cluster Topology (For Visualization)
    CLUSTER_NODES = [
        {
            "id": "node-01", "name": "Core-Master-01", "ip": "10.0.1.10", "type": "Physical",
            "cpu_cores": 16, "ram_gb": 64, "os": "Ubuntu 22.04 LTS",
            "services": ["Auth Service", "ID Service"]
        },
        {
            "id": "node-02", "name": "Sec-Cluster-01", "ip": "10.0.1.11", "type": "Virtual", 
            "cpu_cores": 8, "ram_gb": 32, "os": "Alpine Linux",
            "services": ["Verify Service", "Audit Service"]
        },
        {
            "id": "node-03", "name": "Edge-Gateway-01", "ip": "10.0.2.5", "type": "Container",
            "cpu_cores": 4, "ram_gb": 16, "os": "K3s Node",
            "services": ["IPRS Mock"]
        }
    ]
    
    # Service Base URLs (Mapped for Easy Access)
    AUTH_SERVICE_URL = AUTH_SERVICE_URL
    ID_SERVICE_URL = ID_SERVICE_URL
    VERIFY_SERVICE_URL = VERIFY_SERVICE_URL
    AUDIT_SERVICE_URL = AUDIT_SERVICE_URL
    IPRS_SERVICE_URL = IPRS_SERVICE_URL

    # Auth
    LOGIN = f"{AUTH_SERVICE_URL}/auth/admin/login/"
    AUTH_ADMIN_USERS = f"{AUTH_SERVICE_URL}/auth/admin/users/"
    
    # IPRS (Citizens)
    CITIZENS = f"{IPRS_SERVICE_URL}/citizens/"
    
    # ID Service
    DIGITAL_IDS = f"{ID_SERVICE_URL}/digital_ids/"
    ISSUE_ID = f"{ID_SERVICE_URL}/digital_ids/issue/"
    REQUESTS = f"{ID_SERVICE_URL}/requests/"
    
    # Audit
    AUDIT_LOGS = f"{AUDIT_SERVICE_URL}/audit/logs/"

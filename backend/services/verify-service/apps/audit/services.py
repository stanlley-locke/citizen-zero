import requests

class AuditLogger:
    @staticmethod
    def log(action, user_id, details, status='SUCCESS', severity='INFO', username=None, actor_type='SYSTEM'):
        try:
            # Hardcoded Audit Service URL for MVP
            url = "http://127.0.0.1:8003/api/v1/audit/logs/"
            payload = {
                "action": action,
                "user_id": user_id,
                "username": username,
                "actor_type": actor_type,
                "details": details,
                "status": status,
                "severity": severity,
                "ip_address": "127.0.0.1" # Stub
            }
            # Fire and forget (timeout 1s)
            requests.post(url, json=payload, timeout=1)
        except Exception as e:
            print(f"Failed to log audit: {e}")

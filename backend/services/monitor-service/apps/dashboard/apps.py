from django.apps import AppConfig
import threading
import time
import requests
from django.conf import settings
import os
import shutil
import datetime
from pathlib import Path

# Global In-Memory Store
class MonitorStore:
    services = {} 

store = MonitorStore()

class BackupManager:
    """Handles Real File Backups"""
    BACKUP_ROOT = settings.BASE_DIR / 'backups'

    @staticmethod
    def get_db_path(service_name):
        # settings.BASE_DIR = .../backend/services/monitor-service
        services_dir = settings.BASE_DIR.parent # .../backend/services
        backend_dir = services_dir.parent       # .../backend
        
        if "auth" in service_name.lower(): return services_dir / "auth-service/db.sqlite3"
        if "id" in service_name.lower(): return services_dir / "id-service/db.sqlite3"
        if "verify" in service_name.lower(): return services_dir / "verify-service/db.sqlite3"
        if "audit" in service_name.lower(): return services_dir / "audit-service/db.sqlite3"
        if "iprs" in service_name.lower(): return backend_dir / "iprs-mock/db.sqlite3"
        return None

    @staticmethod
    def create_snapshot(service_name):
        source = BackupManager.get_db_path(service_name)
        if not source or not source.exists():
            return False, "DB File not found"
            
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        dest_dir = BackupManager.BACKUP_ROOT / service_name.replace(" ", "_").lower()
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        dest_file = dest_dir / f"snapshot_{timestamp}.sqlite3"
        shutil.copy2(source, dest_file)
        return True, f"Snapshot created: {dest_file.name}"

    @staticmethod
    def get_latest_snapshot_info(service_name):
        dest_dir = BackupManager.BACKUP_ROOT / service_name.replace(" ", "_").lower()
        if not dest_dir.exists():
            return {"last_snapshot": "No backups yet", "size_mb": 0, "status": "Idle"}
            
        files = list(dest_dir.glob("*.sqlite3"))
        if not files:
            return {"last_snapshot": "No backups yet", "size_mb": 0, "status": "Idle"}
            
        latest = max(files, key=os.path.getctime)
        size_mb = latest.stat().st_size / (1024 * 1024)
        time_str = datetime.datetime.fromtimestamp(latest.stat().st_ctime).strftime("%Y-%m-%d %H:%M")
        
        return {
            "last_snapshot": time_str,
            "size_mb": f"{size_mb:.2f}",
            "status": "Success",
            "file": latest.name
        }

class PollerThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.running = True

    def run(self):
        print(">>> Monitor Poller Started")
        BackupManager.BACKUP_ROOT.mkdir(exist_ok=True)
        while self.running:
            self.poll_services()
            time.sleep(3) 

    def poll_services(self):
        services = settings.MONITORED_SERVICES
        for svc in services:
            name = svc['name']
            url_metrics = svc.get('url')
            url_ping = svc.get('ping')
            
            status_data = {
                "name": name,
                "status": "offline",
                "latency": 0,
                "last_check": time.time(),
                "metrics": {}
            }
            
            # 1. Network Check
            try:
                start = time.time()
                resp = requests.get(url_ping, timeout=2)
                latency = int((time.time() - start) * 1000)
                
                if resp.status_code == 200:
                    status_data["status"] = "online"
                    status_data["latency"] = latency
                    
                    # Try to parse health check response
                    try:
                        health_data = resp.json()
                        # Capture real DB status from service
                        if 'db_status' in health_data:
                            status_data["real_db_status"] = health_data['db_status']
                        
                        # Capture real Resource metrics from service (if available)
                        if 'cpu_percent' in health_data:
                            status_data["remote_resources"] = {
                                "cpu": health_data.get('cpu_percent', 0),
                                "ram": health_data.get('memory_percent', 0),
                                "disk": health_data.get('disk_percent', 0)
                            }
                    except:
                        pass

                    if "monitor/metrics" in url_metrics:
                        try:
                            m = requests.get(url_metrics, timeout=1).json()
                            status_data["metrics"] = m
                            if "recent_traffic" in m:
                                status_data["metrics"]["recent_traffic"] = m["recent_traffic"]
                            
                            # Log success
                            with open("monitor_debug.log", "a") as f:
                                f.write(f"{datetime.datetime.now()} [SUCCESS] {name} metrics loaded. Keys: {list(m.keys())}\n")

                        except Exception as e:
                             with open("monitor_debug.log", "a") as f:
                                f.write(f"{datetime.datetime.now()} [ERROR] {name} metrics failed: {e}\n")
                             pass
                else:
                    status_data["status"] = "error"
                
                # Extract port from URL for display
                try:
                    from urllib.parse import urlparse
                    port = urlparse(url_ping).port
                    status_data["metrics"]["port"] = port
                except Exception as e:
                    with open("monitor_debug.log", "a") as f:
                        f.write(f"{datetime.datetime.now()} [ERROR] {name} port extraction failed: {e}\n")
                    status_data["metrics"]["port"] = "80"

            except Exception as e:
                with open("monitor_debug.log", "a") as f:
                    f.write(f"{datetime.datetime.now()} [CRITICAL] {name} poll failed: {e}\n")
                status_data["status"] = "offline"

            # 2. Real System Resources (psutil) - Local Fallback
            if "remote_resources" in status_data:
                 status_data["resources"] = status_data["remote_resources"]
                 status_data["resources"]["ip"] = "Remote" # Placeholder
            else:
                try:
                    import psutil
                    cpu = psutil.cpu_percent(interval=None) or 1
                    ram = psutil.virtual_memory().percent
                    disk = psutil.disk_usage('/').percent
                except:
                    cpu, ram, disk = 0, 0, 0
                
                # Real IP Address
                try:
                    import socket
                    hostname = socket.gethostname()
                    real_ip = socket.gethostbyname(hostname)
                except:
                    real_ip = "127.0.0.1"
                    
                status_data["resources"] = {
                    "cpu": cpu, 
                    "ram": ram, 
                    "disk": disk,
                    "ip": real_ip 
                }

            # 3. Real Database Stats
            db_path = BackupManager.get_db_path(name)
            db_info = {
                "status": "Unknown",
                "storage_status": "Not Found",
                "size": "0 MB",
                "engine": "SQLite3"
            }
            if db_path and db_path.exists():
                size = db_path.stat().st_size / (1024 * 1024)
                db_info["size"] = f"{size:.2f} MB"
                db_info["storage_status"] = "Mounted"
                
                # Prefer self-reported status, fallback to "connected" if file exists
                if "real_db_status" in status_data:
                    db_info["status"] = status_data["real_db_status"]
                else:
                    db_info["status"] = "connected" if status_data["status"] == "online" else "disconnected"
            
            # If no file path matches (e.g. mock), trust the service anyway
            elif "real_db_status" in status_data:
                 db_info["status"] = status_data["real_db_status"]
                 db_info["storage_status"] = "Remote/Unknown"
            
            status_data["database"] = db_info

            # 4. Real Backup Stats
            status_data["backup"] = BackupManager.get_latest_snapshot_info(name)
            
            store.services[name] = status_data

class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.dashboard'

    def ready(self):
        if os.environ.get('RUN_MAIN') == 'true':
            poller = PollerThread()
            poller.start()

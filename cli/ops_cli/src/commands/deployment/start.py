import os
import time
import subprocess
import json
import questionary
from rich.console import Console
from pathlib import Path

console = Console()

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent.parent
LOGS_DIR = PROJECT_ROOT / "logs"
RUNTIME_DIR = PROJECT_ROOT / "runtime"
PIDS_FILE = RUNTIME_DIR / "services.json"

SERVICES = [
    {"name": "Auth Service", "path": "backend/services/auth-service", "port": 8000, "value": "auth", "log": "auth_service.log"},
    {"name": "ID Service", "path": "backend/services/id-service", "port": 8001, "value": "id", "log": "id_service.log"},
    {"name": "Verify Service", "path": "backend/services/verify-service", "port": 8002, "value": "verify", "log": "verify_service.log"},
    {"name": "Audit Service", "path": "backend/services/audit-service", "port": 8003, "value": "audit", "log": "audit_service.log"},
    {"name": "IPRS Mock", "path": "backend/iprs-mock", "port": 8005, "value": "iprs", "log": "iprs_mock.log"},
    {"name": "Monitor Service", "path": "backend/services/monitor-service", "port": 8006, "value": "monitor", "log": "monitor_service.log"},
]

def save_pid(name, pid):
    data = {}
    if PIDS_FILE.exists():
        try:
            with open(PIDS_FILE, 'r') as f:
                data = json.load(f)
        except:
            pass
    
    data[name] = pid
    
    with open(PIDS_FILE, 'w') as f:
        json.dump(data, f)

def launch_service(service, mode="terminal"):
    name = service["name"]
    rel_path = service["path"]
    port = service["port"]
    log_file = service["log"]
    
    abs_path = PROJECT_ROOT / rel_path
    
    if not abs_path.exists():
        console.print(f"[bold red]Error:[/bold red] Path not found: {abs_path}")
        return

    if mode == "terminal":
        # Windows command: start "Title" cmd /k "cd /d PATH && python command"
        cmd = f'start "{name}" cmd /k "cd /d {abs_path} && python manage.py runserver 0.0.0.0:{port}"'
        console.print(f"Launching [cyan]{name}[/cyan] in new window on port {port}...")
        os.system(cmd)
    
    elif mode == "background":
        log_path = LOGS_DIR / log_file
        console.print(f"Starting [cyan]{name}[/cyan] (Background) -> Logs: {log_file}")
        
        # Open log file
        with open(log_path, "a") as out:
            # We must set shell=False for Popen with list args to work predictably with cwd
            # But we are launching python directly.
            process = subprocess.Popen(
                ["python", "manage.py", "runserver", f"0.0.0.0:{port}"],
                cwd=str(abs_path),
                stdout=out,
                stderr=out,
                shell=False
            )
            
            save_pid(name, process.pid)

def start_services_command():
    # 1. Select Mode
    mode = questionary.select(
        "Select Launch Mode:",
        choices=[
            questionary.Choice("Background Mode (VPS Style)", value="background"),
            questionary.Choice("Terminal Mode (New Windows)", value="terminal"),
            "Cancel"
        ]
    ).ask()
    
    if mode == "Cancel":
        return

    # 2. Select Services
    choices = [
        questionary.Choice("Start All Services", value="all"),
        questionary.Separator(),
    ]
    for s in SERVICES:
        choices.append(questionary.Choice(s["name"], value=s["value"]))
    
    selection = questionary.checkbox(
        "Select services to launch:",
        choices=choices,
        validate=lambda x: "Please select at least one service" if len(x) == 0 else True
    ).ask()

    if not selection:
        return

    to_launch = []
    if "all" in selection:
        to_launch = SERVICES
    else:
        to_launch = [s for s in SERVICES if s["value"] in selection]

    console.print(f"[bold green]Initiating Launch sequence for {len(to_launch)} services...[/bold green]")
    
    # Ensure dirs exist
    if mode == "background":
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    
    for service in to_launch:
        launch_service(service, mode)
        time.sleep(1)

    if mode == "background":
        console.print("\n[bold green]Services running in background.[/bold green]")
        console.print(f"Logs are being written to: [yellow]{LOGS_DIR}[/yellow]")
        console.print("Use 'Stop Services' to shut them down.")
    else:
        console.print("\n[bold green]Done![/bold green] Check the new terminal windows.")

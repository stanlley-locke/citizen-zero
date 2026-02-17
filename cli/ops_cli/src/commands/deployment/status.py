import socket
from rich.console import Console
from rich.table import Table

console = Console()

SERVICES = [
    {"name": "Auth Service", "port": 8000},
    {"name": "ID Service", "port": 8001},
    {"name": "Verify Service", "port": 8002},
    {"name": "Audit Service", "port": 8003},
    {"name": "IPRS Mock", "port": 8005},
    {"name": "Monitor Service", "port": 8006},
]

def check_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex(('127.0.0.1', port)) == 0

def check_services_status_command():
    table = Table(title="Service Connectivity Check")
    table.add_column("Service", style="cyan")
    table.add_column("Port", style="yellow")
    table.add_column("Status")

    with console.status("[bold blue]Pinging ports...[/bold blue]"):
        for service in SERVICES:
            is_open = check_port(service["port"])
            status = "[green]RUNNING[/green]" if is_open else "[red]STOPPED[/red]"
            table.add_row(service["name"], str(service["port"]), status)

    console.print(table)

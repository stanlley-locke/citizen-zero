import requests
from rich.console import Console
from rich.table import Table
from services.api_client import APIClient
from config.settings import AUDIT_SERVICE_URL

console = Console()

def audit_trail_command():
    client = APIClient(AUDIT_SERVICE_URL) # Note: Settings has /audit appended already? Check settings.py
    # settings.py: AUDIT_SERVICE_URL = .../api/v1/audit
    # Audit service urls usually are /logs/
    
    with console.status("[bold green]Fetching Audit Trail...[/bold green]"):
        resp = client.get("logs/")
        
    if not resp or resp.status_code != 200:
        console.print("[red]Failed to fetch audit logs.[/red]")
        return

    data = resp.json()
    logs = data.get('results', data) if isinstance(data, dict) else data

    table = Table(title="System Audit Trail")
    table.add_column("Time", style="cyan")
    table.add_column("Actor", style="blue")
    table.add_column("Action", style="magenta")
    table.add_column("Details")
    table.add_column("Status")

    for log in logs:
        table.add_row(
            log.get('timestamp', '')[:19],
            log.get('username', 'System'),
            log.get('action', 'UNKNOWN'),
            log.get('details', '-'),
            log.get('status', 'INFO')
        )

    console.print(table)

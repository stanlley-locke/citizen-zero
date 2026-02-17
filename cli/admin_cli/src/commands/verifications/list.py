import requests
from rich.console import Console
from rich.table import Table
from services.api_client import APIClient
from config.settings import VERIFY_SERVICE_URL

console = Console()

def list_verifications_command():
    client = APIClient(VERIFY_SERVICE_URL)
    
    with console.status("[bold green]Fetching Verification Logs...[/bold green]"):
        # Verify Service ViewSet: /verifications/ or /logs/ ?
        # Usually standard GenericViewSet is mapped to /verifications/
        resp = client.get("verifications/")
        
    if not resp or resp.status_code != 200:
        console.print("[red]Failed to fetch logs.[/red]")
        return

    data = resp.json()
    logs = data.get('results', data) if isinstance(data, dict) else data

    table = Table(title="Verification Activity")
    table.add_column("Time", style="cyan")
    table.add_column("Verifier", style="blue")
    table.add_column("Document", style="yellow")
    table.add_column("Result")

    for log in logs:
        status_style = "green" if log.get('status') == 'VALID' else "red"
        table.add_row(
            log.get('timestamp', '')[:19],
            log.get('verifier_id', 'Unknown'),
            log.get('document_number', 'N/A'),
            f"[{status_style}]{log.get('status', 'UNKNOWN')}[/{status_style}]"
        )

    console.print(table)

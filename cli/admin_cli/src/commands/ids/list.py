import requests
from rich.console import Console
from rich.table import Table
from services.api_client import APIClient
from config.settings import ID_SERVICE_URL

console = Console()

def list_ids_command():
    client = APIClient(ID_SERVICE_URL)
    
    with console.status("[bold green]Fetching Issued IDs...[/bold green]"):
        # Based on ID Service views: DigitalIDViewSet is at /digital-ids/
        resp = client.get("digital-ids/")
        
    if not resp or resp.status_code != 200:
        console.print("[red]Failed to fetch IDs.[/red]")
        return

    data = resp.json()
    ids = data.get('results', data) if isinstance(data, dict) else data

    table = Table(title="Issued Identity Documents")
    table.add_column("Document No", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Status", style="green")
    table.add_column("Issued At")

    for doc in ids:
        table.add_row(
            doc.get('document_number', 'N/A'),
            doc.get('document_type', 'UNKNOWN').replace('_', ' ').title(),
            doc.get('status', 'ACTIVE'),
            doc.get('issued_at', '')[:10] # Truncate date
        )

    console.print(table)

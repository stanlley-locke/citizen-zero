import requests
from rich.console import Console
from rich.table import Table
from services.api_client import APIClient
from config.settings import ID_SERVICE_URL

console = Console()

def list_citizens_command():
    client = APIClient(ID_SERVICE_URL)
    
    # We use the proxy endpoint in ID Service that forwards to IPRS
    # Or directly talk to IPRS if configured. 
    # Based on views.py in ID service, there is a CitizenProxyViewSet at /citizens/
    
    with console.status("[bold green]Fetching Citizens...[/bold green]"):
        resp = client.get("citizens/")
        
    if not resp or resp.status_code != 200:
        console.print("[red]Failed to fetch citizens.[/red]")
        return

    data = resp.json()
    # Handle pagination if present (e.g. { "results": [...] })
    citizens = data.get('results', data) if isinstance(data, dict) else data

    table = Table(title="Registered Citizens")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("National ID", style="green")
    table.add_column("Phone")
    table.add_column("Status")

    for citizen in citizens:
        table.add_row(
            str(citizen.get('id', '')),
            f"{citizen.get('first_name')} {citizen.get('last_name')}",
            citizen.get('national_id', 'N/A'),
            citizen.get('phone_number', 'N/A'),
            "Active" # Mock status
        )

    console.print(table)

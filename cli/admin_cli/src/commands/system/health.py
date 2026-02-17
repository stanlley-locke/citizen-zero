import requests
from rich.console import Console
from rich.table import Table
from services.api_client import APIClient
from config.settings import MONITOR_SERVICE_URL

console = Console()

def system_health_command():
    client = APIClient(MONITOR_SERVICE_URL)
    
    with console.status("[bold green]Diagnosing System Health...[/bold green]"):
        resp = client.get("stats/")
        
    if not resp or resp.status_code != 200:
        console.print("[red]Failed to fetch system stats.[/red]")
        return

    data = resp.json()
    
    # Summary
    summary = data.get('summary', {})
    console.print(f"\n[bold]Total Services:[/bold] {summary.get('total')}")
    console.print(f"[bold]Online:[/bold] [green]{summary.get('online')}[/green]")
    console.print(f"[bold]Health Score:[/bold] {summary.get('healthy_percentage')}%\n")

    table = Table(title="Service Status")
    table.add_column("Service", style="cyan")
    table.add_column("Status", style="magenta")
    table.add_column("Latency")

    for node in data.get("nodes", []):
         status = node.get("status", "offline")
         style = "green" if status == "online" else "red"
         table.add_row(
             node.get("label"),
             f"[{style}]{status.upper()}[/{style}]",
             f"{node.get('latency')}ms"
         )

    console.print(table)

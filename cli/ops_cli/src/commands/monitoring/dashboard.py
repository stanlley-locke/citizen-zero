import time
import requests
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from config.settings import MONITOR_SERVICE_URL # We need to ensure config is accessible

console = Console()

# We might need to duplicate settings or import from admin_cli if strictly separated. 
# For now let's assume valid import or hardcode for MVP proof.
MONITOR_API = "http://127.0.0.1:8006/api/v1/monitor/stats/"

def fetch_stats():
    try:
        resp = requests.get(MONITOR_API, timeout=2)
        if resp.status_code == 200:
            return resp.json()
    except:
        pass
    return None

def generate_table(data):
    table = Table(title="System Health")
    table.add_column("Service", style="cyan")
    table.add_column("Status", style="magenta")
    table.add_column("Latency (ms)", justify="right")
    table.add_column("CPU %", justify="right")
    table.add_column("RAM %", justify="right")
    
    if not data or "nodes" not in data:
        table.add_row("System", "OFFLINE", "-", "-", "-")
        return table

    for node in data.get("nodes", []):
        status = node.get("status", "offline")
        status_style = "green" if status == "online" else "red"
        
        table.add_row(
            node.get("label", "Unknown"),
            f"[{status_style}]{status.upper()}[/{status_style}]",
            str(node.get("latency", 0)),
            str(node.get("cpu_percent", 0)),
            str(node.get("memory_percent", 0))
        )
    return table

def monitoring_dashboard_command():
    console.clear()
    console.print(Panel("Starting Live Monitor... (Press Ctrl+C to stop)", style="blue"))
    try:
        with Live(generate_table(None), refresh_per_second=1) as live:
            while True:
                data = fetch_stats()
                live.update(generate_table(data))
                time.sleep(2)
    except KeyboardInterrupt:
        console.print("[yellow]Stopped.[/yellow]")

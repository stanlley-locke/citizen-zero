import os
import signal
import json
import questionary
from rich.console import Console
from pathlib import Path
import psutil # Better process management

console = Console()

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent.parent
RUNTIME_DIR = PROJECT_ROOT / "runtime"
PIDS_FILE = RUNTIME_DIR / "services.json"

def kill_process_tree(pid):
    try:
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        for child in children:
            child.kill()
        parent.kill()
        return True
    except psutil.NoSuchProcess:
        return False
    except Exception as e:
        console.print(f"[red]Error killing {pid}: {e}[/red]")
        return False

def stop_services_command():
    if not PIDS_FILE.exists():
        console.print("[yellow]No active services found (pids file missing).[/yellow]")
        return

    try:
        with open(PIDS_FILE, 'r') as f:
            data = json.load(f)
    except:
        console.print("[red]Corrupt PIDs file.[/red]")
        return
    
    if not data:
        console.print("[yellow]No active services tracked.[/yellow]")
        return

    choices = [questionary.Choice("Stop All", value="all")] + list(data.keys())
    
    selection = questionary.checkbox(
        "Select services to STOP:",
        choices=choices
    ).ask()
    
    if not selection:
        return
        
    to_stop = []
    if "all" in selection:
        to_stop = list(data.keys())
    else:
        to_stop = selection

    with console.status("[bold red]Stopping services...[/bold red]"):
        new_data = data.copy()
        for name in to_stop:
            pid = data.get(name)
            if pid:
                console.print(f"Stopping {name} (PID: {pid})...")
                # Attempt to kill
                success = kill_process_tree(pid)
                if success:
                    console.print(f"[green]✔ {name} stopped.[/green]")
                else:
                    console.print(f"[yellow]⚠ {name} (PID {pid}) not found or already stopped.[/yellow]")
                
                # Remove from tracking
                del new_data[name]
    
    # Save updated list
    with open(PIDS_FILE, 'w') as f:
        json.dump(new_data, f)
        
    console.print("[green]Process Complete.[/green]")

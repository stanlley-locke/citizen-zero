import questionary
from rich.console import Console
from services.api_client import APIClient
from config.settings import AUTH_SERVICE_URL

console = Console()

def login_command():
    console.print("[bold blue]Authentication[/bold blue]")
    
    username = questionary.text("Username:").ask()
    password = questionary.password("Password:").ask()
    
    if not username or not password:
        console.print("[red]Username and password required.[/red]")
        return

    # Use a spinner
    with console.status("[bold green]Authenticating...[/bold green]"):
        client = APIClient(AUTH_SERVICE_URL)
        # Use the Admin Login endpoint
        success, msg = client.login(username, password, f"{AUTH_SERVICE_URL}/admin/login/")
    
    if success:
        console.print(f"[green]✔ {msg}[/green]")
    else:
        console.print(f"[red]✘ {msg}[/red]")

import questionary
from rich.console import Console
from services.api_client import APIClient
from config.settings import ID_SERVICE_URL

console = Console()

def add_citizen_command():
    console.print("[bold blue]Register New Citizen[/bold blue]")
    
    # Form Wizard
    first_name = questionary.text("First Name:").ask()
    last_name = questionary.text("Last Name:").ask()
    national_id = questionary.text("National ID Number:").ask()
    date_of_birth = questionary.text("Date of Birth (YYYY-MM-DD):").ask()
    gender = questionary.select("Gender:", choices=["Male", "Female", "Other"]).ask()
    phone = questionary.text("Phone Number:").ask()
    email = questionary.text("Email:").ask()

    if not national_id:
        console.print("[red]Operation cancelled.[/red]")
        return

    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "national_id": national_id,
        "date_of_birth": date_of_birth,
        "gender": gender,
        "phone_number": phone,
        "email": email
    }

    client = APIClient(ID_SERVICE_URL)
    
    with console.status("[bold green]Registering...[/bold green]"):
        # Accessing the proxy endpoint
        resp = client.post("citizens/", data=payload)

    if resp and resp.status_code in [200, 201]:
        console.print(f"[green]✔ Citizen {first_name} {last_name} registered successfully![/green]")
    else:
        console.print(f"[red]✘ Registration Failed[/red]")
        if resp:
            console.print(resp.text)

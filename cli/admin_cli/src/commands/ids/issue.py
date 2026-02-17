import questionary
from rich.console import Console
from services.api_client import APIClient
from config.settings import ID_SERVICE_URL

console = Console()

def issue_id_command():
    console.print("[bold blue]Issue New Identity Document[/bold blue]")
    
    # Simple wizard
    citizen_id = questionary.text("Citizen Internal ID (UUID):").ask()
    doc_type = questionary.select(
        "Document Type:",
        choices=["NATIONAL_ID", "PASSPORT", "DRIVING_LICENSE", "HEALTH_CERTIFICATE"]
    ).ask()
    
    if not citizen_id:
        console.print("[red]Cancelled.[/red]")
        return

    payload = {
        "citizen_id": citizen_id,
        "document_type": doc_type,
        "status": "APPROVED" # Auto-approve for CLI
    }

    client = APIClient(ID_SERVICE_URL)
    
    with console.status("[bold green]Issuing Document...[/bold green]"):
        # We use the IssuanceRequest endpoint to trigger the flow
        resp = client.post("issuance-requests/", data=payload)

    if resp and resp.status_code in [200, 201]:
        console.print(f"[green]✔ Request submitted for {doc_type}![/green]")
    else:
        console.print(f"[red]✘ Failed to issue ID[/red]")
        if resp:
            console.print(resp.text)

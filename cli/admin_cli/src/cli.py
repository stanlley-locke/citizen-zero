import questionary
from rich.console import Console
from rich.panel import Panel
from commands.auth.login import login_command
from config.settings import APP_NAME, VERSION
from commands.auth.login import login_command
from services.api_client import APIClient
from config.settings import APP_NAME, VERSION, AUTH_SERVICE_URL, TOKENS_FILE
import os

console = Console()

def print_header(username=None):
    subtitle = f"[cyan]Logged in as: {username}[/cyan]" if username else "[red]Not Logged In[/red]"
    console.print(Panel(f"[bold green]{APP_NAME}[/bold green] v{VERSION}\n{subtitle}", expand=False))

def logout_command():
    if os.path.exists(TOKENS_FILE):
        os.remove(TOKENS_FILE)
    console.print("[yellow]Logged out successfully.[/yellow]")

def main_menu():
    while True:
        # Check auth state
        client = APIClient(AUTH_SERVICE_URL)
        is_auth = client.is_authenticated()
        
        # Determine current user (could be extracted from token in real JWT, here we just guess/persist)
        # For simple UI, just show auth status.
        username = "Admin" if is_auth else None
        
        console.clear()
        print_header(username)
        
        if not is_auth:
            choices = [
                "Login",
                "System Health",
                questionary.Separator(),
                "Exit"
            ]
        else:
            choices = [
                "Manage Citizens",
                "Manage IDs",
                "Verifications",
                "Audit Logs",
                "System Health",
                questionary.Separator(),
                "Logout",
                "Exit"
            ]

        choice = questionary.select(
            "What would you like to do?",
            choices=choices
        ).ask()
        
        if choice == "Login":
            login_command()
            input("\nPress Enter to continue...")
        elif choice == "Logout":
            logout_command()
            input("\nPress Enter to continue...")
            
        elif choice == "Manage Citizens":
            action = questionary.select(
                "Citizen Management",
                choices=["List Citizens", "Register Citizen", "Back"]
            ).ask()
            
            if action == "List Citizens":
                from commands.citizens.list import list_citizens_command
                list_citizens_command()
            elif action == "Register Citizen":
                from commands.citizens.add import add_citizen_command
                add_citizen_command()
            input("\nPress Enter to continue...")
        
        elif choice == "Manage IDs":
            action = questionary.select(
                "ID Management",
                choices=["List Issued IDs", "Issue New ID", "Back"]
            ).ask()
            
            if action == "List Issued IDs":
                from commands.ids.list import list_ids_command
                list_ids_command()
            elif action == "Issue New ID":
                from commands.ids.issue import issue_id_command
                issue_id_command()
            input("\nPress Enter to continue...")
                
        elif choice == "Verifications":
             from commands.verifications.list import list_verifications_command
             list_verifications_command()
             input("\nPress Enter to continue...")
             
        elif choice == "Audit Logs":
             from commands.audit.trail import audit_trail_command
             audit_trail_command()
             input("\nPress Enter to continue...")

        elif choice == "System Health":
             from commands.system.health import system_health_command
             system_health_command()
             input("\nPress Enter to continue...")
             
        elif choice == "Exit":
            console.print("[yellow]Goodbye![/yellow]")
            break
            
def app():
    main_menu()

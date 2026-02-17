import questionary
from rich.console import Console
from rich.panel import Panel
from commands.monitoring.dashboard import monitoring_dashboard_command

console = Console()

def print_header():
    console.print(Panel("[bold blue]Citizen-Zero Ops CLI[/bold blue]", expand=False))

def main_menu():
    print_header()
    while True:
        choice = questionary.select(
            "Operations Menu",
            choices=[
                "System Monitoring",
                "Deployment Status",
                "Start Services",
                "Stop Services",
                questionary.Separator(),
                "Exit"
            ]
        ).ask()
        
        if choice == "System Monitoring":
            monitoring_dashboard_command()
        elif choice == "Deployment Status":
            from commands.deployment.status import check_services_status_command
            check_services_status_command()
        elif choice == "Start Services":
            from commands.deployment.start import start_services_command
            start_services_command()
        elif choice == "Stop Services":
            from commands.deployment.stop import stop_services_command
            stop_services_command()
        elif choice == "Exit":
            console.print("[yellow]Goodbye![/yellow]")
            break

def app():
    main_menu()

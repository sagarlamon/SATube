import questionary
from rich.console import Console
from rich.table import Table
from satube.history import history_manager

console = Console()

def show_history() -> None:
    """Displays and manages the download history."""
    while True:
        records = history_manager.get_all()
        if not records:
            console.print("[yellow]Your download history is empty.[/yellow]")
            questionary.press_any_key_to_continue().ask()
            return

        table = Table(title="Download History", box=None, header_style="bold magenta")
        table.add_column("ID", justify="right", style="cyan", no_wrap=True)
        table.add_column("Date", style="green")
        table.add_column("Type", style="yellow")
        table.add_column("Title", style="white")
        table.add_column("Size", style="blue")

        for idx, rec in enumerate(records, start=1):
            title = rec['title']
            if len(title) > 40:
                title = title[:37] + "..."
            table.add_row(str(idx), rec['timestamp'], rec['type'], title, rec['size'])

        console.print()
        console.print(table)
        console.print()

        action = questionary.select(
            "History Options:",
            choices=["Search", "Clear All History", "Back to Menu"]
        ).ask()

        if action == "Search":
            query = questionary.text("Enter search term:").ask()
            results = history_manager.search(query)
            console.print(f"\n[cyan]Found {len(results)} results.[/cyan]\n")
        elif action == "Clear All History":
            confirm = questionary.confirm("Are you sure you want to clear all history?").ask()
            if confirm:
                history_manager.clear()
                console.print("[bold green]History cleared![/bold green]")
        else:
            break
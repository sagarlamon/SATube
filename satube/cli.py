import typer
import questionary
from rich.console import Console
from satube.utils import clear_screen
from satube.commands.video import download_video_interactive
from satube.commands.audio import download_audio_interactive
from satube.commands.info import show_video_info, show_available_formats
from satube.commands.history import show_history
from satube.commands.settings import manage_settings
from satube.commands.queue import manage_queue
from satube.commands.update import update_ytdlp

app = typer.Typer(help="SATube: Fast, Beautiful, Open Source Media Downloader.")
console = Console()

LOGO = """
╭──────────────────────────────────────╮
│                                      │
│  ███████╗  █████╗ ████████╗██╗   ██╗ │
│  ██╔════╝ ██╔══██╗╚══██╔══╝██║   ██║ │
│  ███████╗ ███████║   ██║   ██║   ██║ │
│  ╚════██║ ██╔══██║   ██║   ██║   ██║ │
│  ███████║ ██║  ██║   ██║   ╚██████╔╝ │
│  ╚══════╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝  │
│                                      │
│               SATube v1.0            │
│      Fast • Beautiful • Open Source  │
╰──────────────────────────────────────╯
"""

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """Main entry point for SATube dashboard."""
    if ctx.invoked_subcommand is None:
        interactive_menu()

def interactive_menu() -> None:
    while True:
        clear_screen()
        console.print(f"[bold cyan]{LOGO}[/bold cyan]")
        
        choices = [
            "Download Video",
            "Download Audio",
            "Video Information",
            "Available Formats",
            "Queue Manager",
            "Download History",
            "Settings",
            "Update yt-dlp",
            "Exit"
        ]
        
        action = questionary.select(
            "Main Menu:",
            choices=choices,
            use_indicator=True
        ).ask()
        
        if action == "Download Video":
            download_video_interactive()
        elif action == "Download Audio":
            download_audio_interactive()
        elif action == "Video Information":
            show_video_info()
            questionary.press_any_key_to_continue().ask()
        elif action == "Available Formats":
            show_available_formats()
            questionary.press_any_key_to_continue().ask()
        elif action == "Queue Manager":
            manage_queue()
        elif action == "Download History":
            show_history()
        elif action == "Settings":
            manage_settings()
        elif action == "Update yt-dlp":
            update_ytdlp()
            questionary.press_any_key_to_continue().ask()
        elif action == "Exit" or action is None:
            console.print("[bold green]Thank you for using SATube![/bold green]")
            break

if __name__ == "__main__":
    app()
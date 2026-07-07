import subprocess
import sys
from rich.console import Console

console = Console()

def update_ytdlp() -> None:
    """Updates yt-dlp via pip."""
    with console.status("[bold cyan]Updating yt-dlp...", spinner="dots"):
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"], check=True, capture_output=True)
            console.print("[bold green]Successfully updated yt-dlp to the latest version![/bold green]")
        except subprocess.CalledProcessError as e:
            console.print(f"[bold red]Failed to update yt-dlp: {e.stderr.decode()}[/bold red]")
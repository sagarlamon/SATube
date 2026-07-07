from typing import Optional
import questionary
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from satube.downloader import downloader
from satube.utils import is_valid_url, format_duration
from satube.logger import logger

console = Console()

def _prompt_url() -> Optional[str]:
    """Prompts the user for a URL and validates it."""
    url = questionary.text("Enter video URL:").ask()
    if not url:
        return None
    if not is_valid_url(url):
        console.print("[bold red]Error: Invalid URL format.[/bold red]")
        return None
    return url

def show_video_info(url: Optional[str] = None) -> None:
    """Fetches and displays comprehensive metadata for a given video URL."""
    if not url:
        url = _prompt_url()
    if not url:
        return

    with console.status("[bold cyan]Fetching video information...", spinner="dots"):
        info = downloader.extract_info(url)

    if not info:
        console.print("[bold red]Failed to fetch video information. Please check the URL or your network connection.[/bold red]")
        return

    # Extract relevant metadata
    title = info.get('title', 'Unknown Title')
    uploader = info.get('uploader', 'Unknown Uploader')
    duration = format_duration(info.get('duration', 0))
    view_count = f"{info.get('view_count', 0):,}" if info.get('view_count') else "Unknown"
    upload_date = info.get('upload_date', 'Unknown')
    if upload_date and len(upload_date) == 8:
        # Format YYYYMMDD to YYYY-MM-DD
        upload_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}"
    
    # Description logic (truncate if too long)
    description = info.get('description', 'No description available.')
    if len(description) > 300:
        description = description[:297] + "..."

    # Build the Rich Table for metadata
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Property", style="bold cyan")
    table.add_column("Value", style="white")

    table.add_row("Uploader:", uploader)
    table.add_row("Duration:", duration)
    table.add_row("Views:", view_count)
    table.add_row("Uploaded:", upload_date)
    table.add_row("URL:", url)

    # Render as a Panel
    panel = Panel(
        table,
        title=f"[bold green]{title}[/bold green]",
        subtitle="[dim]Metadata[/dim]",
        expand=False,
        border_style="cyan"
    )

    console.print()
    console.print(panel)
    
    # Print description separately so it doesn't break the table layout
    console.print("\n[bold cyan]Description:[/bold cyan]")
    console.print(Text(description, style="dim"))
    console.print()


def show_available_formats(url: Optional[str] = None) -> None:
    """Fetches and displays a beautifully formatted table of available download formats."""
    if not url:
        url = _prompt_url()
    if not url:
        return

    with console.status("[bold cyan]Fetching available formats...", spinner="dots"):
        formats = downloader.get_formats(url)

    if not formats:
        console.print("[bold red]Failed to fetch formats. Please check the URL or your network connection.[/bold red]")
        return

    table = Table(
        title="Available Formats", 
        box=None, 
        header_style="bold magenta", 
        border_style="dim", 
        row_styles=["none", "dim"]
    )
    
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Ext", style="green")
    table.add_column("Resolution", style="yellow")
    table.add_column("Size", style="blue")
    table.add_column("Video Codec")
    table.add_column("Audio Codec")

    for f in formats:
        table.add_row(
            str(f['format_id']),
            f['ext'],
            f['resolution'],
            f['filesize'],
            f['vcodec'],
            f['acodec']
        )

    console.print()
    console.print(table)
    console.print()
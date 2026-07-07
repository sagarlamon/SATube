import os
import questionary
from rich.console import Console
from satube.downloader import downloader
from satube.history import history_manager
from satube.config import config
from satube.utils import is_valid_url, send_notification, open_folder
from satube.commands.info import show_video_info

console = Console()

def download_audio_interactive() -> None:
    """Guides the user through downloading audio."""
    while True:
        url = questionary.text("Enter Video/Audio URL (or leave blank to exit):").ask()
        if not url:
            break
        if not is_valid_url(url):
            console.print("[bold red]Invalid URL.[/bold red]")
            continue

        show_video_info(url)
        
        formats = ["MP3", "M4A", "FLAC", "WAV", "Original"]
        audio_format = questionary.select(
            f"Choose format (Default: {config.get('default_audio_format')}):",
            choices=formats,
            default=config.get('default_audio_format')
        ).ask()

        if not audio_format:
            break

        bitrate = "320"
        if audio_format not in ["FLAC", "WAV", "Original"]:
            bitrate = questionary.select("Choose bitrate:", choices=["320", "256", "192", "128"]).ask()

        result = downloader.download_audio(url, audio_format, bitrate)

        if result.get("success"):
            filepath = result.get("filepath", "Unknown location")
            size = os.path.getsize(filepath) if os.path.exists(filepath) else 0
            human_size = f"{size / (1024*1024):.2f} MB" if size else "Unknown"
            
            console.print(f"\n[bold green]Download Complete![/bold green]")
            console.print(f"Path: {filepath}")
            
            history_manager.add_entry(url, "Audio", filepath, human_size)
            send_notification("SATube", "Audio download completed!")
            
            next_action = questionary.select(
                "What next?",
                choices=["Download another audio", "Open download folder", "Main menu"]
            ).ask()
            
            if next_action == "Open download folder":
                open_folder(os.path.dirname(filepath))
                break
            elif next_action == "Main menu":
                break
        else:
            console.print(f"[bold red]Download Failed:[/bold red] {result.get('error')}")
            break
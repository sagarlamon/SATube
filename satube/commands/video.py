import os
import questionary
from rich.console import Console
from satube.downloader import downloader
from satube.history import history_manager
from satube.config import config
from satube.utils import is_valid_url, send_notification, open_folder
from satube.commands.info import show_video_info

console = Console()

def download_video_interactive() -> None:
    """Guides the user through downloading a video."""
    while True:
        url = questionary.text("Enter Video URL (or leave blank to exit):").ask()
        if not url:
            break
        if not is_valid_url(url):
            console.print("[bold red]Invalid URL.[/bold red]")
            continue

        # Show info
        show_video_info(url)
        
        quality_choices = ["Best", "2160p", "1440p", "1080p", "720p", "480p", "360p", "Custom"]
        quality = questionary.select(
            f"Choose quality (Default: {config.get('default_quality')}):",
            choices=quality_choices,
            default=config.get('default_quality')
        ).ask()

        if not quality:
            break

        custom_id = None
        if quality == "Custom":
            formats = downloader.get_formats(url)
            if formats:
                choices = [f"{f['format_id']} - {f['ext']} ({f['resolution']}) - {f['filesize']}" for f in formats]
                selected_format = questionary.select("Select exact format:", choices=choices).ask()
                if selected_format:
                    custom_id = selected_format.split(" - ")[0]

        result = downloader.download_video(url, quality, custom_id)

        if result.get("success"):
            filepath = result.get("filepath", "Unknown location")
            size = os.path.getsize(filepath) if os.path.exists(filepath) else 0
            human_size = f"{size / (1024*1024):.2f} MB" if size else "Unknown"
            
            console.print(f"\n[bold green]Download Complete![/bold green]")
            console.print(f"Path: {filepath}")
            
            history_manager.add_entry(url, "Video", filepath, human_size)
            send_notification("SATube", "Video download completed!")
            
            next_action = questionary.select(
                "What next?",
                choices=["Download another video", "Open download folder", "Main menu"]
            ).ask()
            
            if next_action == "Open download folder":
                open_folder(os.path.dirname(filepath))
                break
            elif next_action == "Main menu":
                break
        else:
            console.print(f"[bold red]Download Failed:[/bold red] {result.get('error')}")
            break
import questionary
from rich.console import Console
from satube.config import config

console = Console()

def manage_settings() -> None:
    """Interactive menu to update configuration settings."""
    while True:
        choices = [
            f"Video Folder: {config.get('default_video_folder')}",
            f"Audio Folder: {config.get('default_audio_folder')}",
            f"Default Video Quality: {config.get('default_quality')}",
            f"Default Audio Format: {config.get('default_audio_format')}",
            f"Embed Metadata: {'Yes' if config.get('embed_metadata') else 'No'}",
            f"Desktop Notifications: {'Yes' if config.get('notifications_enabled') else 'No'}",
            "Back to Main Menu"
        ]
        
        selection = questionary.select("Settings:", choices=choices).ask()
        
        if not selection or "Back" in selection:
            break
            
        if "Video Folder" in selection:
            new_val = questionary.path("Enter new video folder path:").ask()
            if new_val: config.set("default_video_folder", new_val)
        elif "Audio Folder" in selection:
            new_val = questionary.path("Enter new audio folder path:").ask()
            if new_val: config.set("default_audio_folder", new_val)
        elif "Video Quality" in selection:
            new_val = questionary.select("Select default video quality:", 
                choices=["Best", "2160p", "1440p", "1080p", "720p", "480p", "360p"]).ask()
            if new_val: config.set("default_quality", new_val)
        elif "Audio Format" in selection:
            new_val = questionary.select("Select default audio format:", 
                choices=["MP3", "M4A", "FLAC", "WAV", "Original"]).ask()
            if new_val: config.set("default_audio_format", new_val)
        elif "Embed Metadata" in selection:
            new_val = questionary.confirm("Embed metadata into files?").ask()
            config.set("embed_metadata", new_val)
        elif "Notifications" in selection:
            new_val = questionary.confirm("Enable desktop notifications?").ask()
            config.set("notifications_enabled", new_val)
            
        console.print("[bold green]Setting updated.[/bold green]")
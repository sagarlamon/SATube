import questionary
from rich.console import Console
from satube.queue import queue_manager, QueueStatus
from satube.downloader import downloader

console = Console()

def manage_queue() -> None:
    while True:
        items = queue_manager.get_all()
        console.print(f"\n[bold]Current Queue ({len(items)} items)[/bold]")
        for idx, item in enumerate(items, 1):
            console.print(f"{idx}. [{item.status.value}] {item.url} ({item.media_type})")
            
        action = questionary.select("Queue Menu:", choices=[
            "Add URL", "Start Queue", "Clear Queue", "Back"
        ]).ask()
        
        if action == "Add URL":
            url = questionary.text("Paste URL:").ask()
            m_type = questionary.select("Type:", choices=["video", "audio"]).ask()
            if url: queue_manager.add(url, m_type)
        elif action == "Start Queue":
            process_queue()
        elif action == "Clear Queue":
            queue_manager.clear()
        else:
            break

def process_queue() -> None:
    while queue_manager.has_pending():
        item = queue_manager.get_next_pending()
        if not item: break
        item.status = QueueStatus.DOWNLOADING
        console.print(f"\n[bold cyan]Processing Queue: {item.url}[/bold cyan]")
        if item.media_type == "video":
            res = downloader.download_video(item.url, "1080p")
        else:
            res = downloader.download_audio(item.url, "MP3", "320")
            
        if res.get("success"):
            item.status = QueueStatus.COMPLETED
        else:
            item.status = QueueStatus.FAILED
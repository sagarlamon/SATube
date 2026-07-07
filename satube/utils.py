import os
import re
import platform
import subprocess
from satube.config import config
from satube.logger import logger

def clear_screen() -> None:
    """Clears the terminal screen."""
    os.system("clear" if os.name == "posix" else "cls")

def is_valid_url(url: str) -> bool:
    """
    Validates if a string is a well-formed HTTP/HTTPS URL.
    This helps prevent yt-dlp from crashing on malformed input.
    """
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
        r'localhost|' # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

def format_duration(seconds: int) -> str:
    """Converts seconds into a human-readable HH:MM:SS format."""
    if not seconds:
        return "Unknown"
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"

def format_size(bytes_size: int) -> str:
    """Converts bytes to a human-readable size (KB, MB, GB)."""
    if not bytes_size:
        return "Unknown Size"
        
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"

def send_notification(title: str, message: str) -> None:
    """
    Sends a native desktop notification if enabled in config.
    Supports Linux (notify-send), macOS (osascript), and Windows (PowerShell).
    """
    if not config.get("notifications_enabled"):
        return

    system = platform.system()
    try:
        if system == "Linux":
            subprocess.run(["notify-send", title, message], check=True)
        elif system == "Darwin": # macOS
            apple_script = f'display notification "{message}" with title "{title}"'
            subprocess.run(["osascript", "-e", apple_script], check=True)
        elif system == "Windows":
            # Basic fallback for Windows using PowerShell
            ps_script = (
                f"[reflection.assembly]::loadwithpartialname('System.Windows.Forms');"
                f"[reflection.assembly]::loadwithpartialname('System.Drawing');"
                f"$notify = new-object system.windows.forms.notifyicon;"
                f"$notify.icon = [System.Drawing.SystemIcons]::Information;"
                f"$notify.visible = $true;"
                f"$notify.showballoontip(10, '{title}', '{message}', [system.windows.forms.tooltipicon]::None)"
            )
            subprocess.run(["powershell", "-Command", ps_script], check=True)
    except Exception as e:
        logger.error(f"Failed to send desktop notification: {e}")

def open_folder(path: str) -> None:
    """Opens the file manager to the specified directory."""
    system = platform.system()
    try:
        if system == "Linux":
            subprocess.run(["xdg-open", path], check=True)
        elif system == "Darwin":
            subprocess.run(["open", path], check=True)
        elif system == "Windows":
            os.startfile(path)
    except Exception as e:
        logger.error(f"Failed to open folder {path}: {e}")
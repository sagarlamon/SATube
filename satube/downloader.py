import os
from pathlib import Path
from typing import Any, Dict, List, Optional
import yt_dlp
from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
    DownloadColumn,
    TransferSpeedColumn,
    TimeRemainingColumn,
)

from satube.config import config
from satube.logger import logger
from satube.utils import format_size

class YTDLPLogger:
    """Intercepts yt-dlp internal logs and routes them to our application logger."""
    def debug(self, msg: str) -> None:
        if not msg.startswith("[debug]"):
            logger.debug(f"yt-dlp: {msg}")

    def info(self, msg: str) -> None:
        logger.info(f"yt-dlp: {msg}")

    def warning(self, msg: str) -> None:
        logger.warning(f"yt-dlp: {msg}")

    def error(self, msg: str) -> None:
        logger.error(f"yt-dlp: {msg}")

class Downloader:
    """Handles metadata extraction and downloading using yt-dlp with rich progress bars."""

    def __init__(self) -> None:
        self.base_opts = {
            'logger': YTDLPLogger(),
            'quiet': True,
            'noprogress': True,
            'no_warnings': True,
        }

    def extract_info(self, url: str) -> Optional[Dict[str, Any]]:
        """Fetches metadata for a URL without downloading it."""
        opts = self.base_opts.copy()
        opts['extract_flat'] = False
        opts['skip_download'] = True

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info
        except yt_dlp.utils.DownloadError as e:
            logger.error(f"Failed to extract info for {url}: {e}")
            return None
        except Exception as e:
            logger.exception(f"Unexpected error during info extraction: {e}")
            return None

    def get_formats(self, url: str) -> List[Dict[str, Any]]:
        """Retrieves a list of available formats for a given video."""
        info = self.extract_info(url)
        if not info or 'formats' not in info:
            return []

        formats = []
        for f in info['formats']:
            # Filter out formats without video or audio to keep the list clean
            if f.get('vcodec') != 'none' or f.get('acodec') != 'none':
                formats.append({
                    'format_id': f.get('format_id', 'N/A'),
                    'ext': f.get('ext', 'N/A'),
                    'resolution': f.get('resolution', 'Audio Only' if f.get('vcodec') == 'none' else 'Unknown'),
                    'filesize': format_size(f.get('filesize') or f.get('filesize_approx') or 0),
                    'vcodec': f.get('vcodec', 'none'),
                    'acodec': f.get('acodec', 'none'),
                })
        return formats

    def _get_postprocessors(self, media_type: str, audio_format: str = "mp3", bitrate: str = "320") -> List[Dict[str, Any]]:
        """Generates the required FFmpeg postprocessors based on config."""
        postprocessors = []

        if media_type == "audio":
            postprocessors.append({
                'key': 'FFmpegExtractAudio',
                'preferredcodec': audio_format.lower() if audio_format.lower() != 'original' else 'best',
                'preferredquality': bitrate,
            })

        if config.get("embed_metadata"):
            postprocessors.append({'key': 'FFmpegMetadata'})

        if config.get("embed_thumbnail"):
            postprocessors.append({'key': 'EmbedThumbnail'})

        return postprocessors

    def _download_with_progress(self, url: str, ydl_opts: Dict[str, Any], title: str) -> Dict[str, Any]:
        """Internal method to execute download while rendering a rich progress bar."""
        result = {"success": False, "filepath": "", "error": ""}

        # Configure Rich progress bar
        progress = Progress(
            TextColumn("[bold cyan]{task.description}"),
            BarColumn(bar_width=40),
            "[progress.percentage]{task.percentage:>3.1f}%",
            "•",
            DownloadColumn(),
            "•",
            TransferSpeedColumn(),
            "•",
            TimeRemainingColumn(),
            transient=True  # Disappears when done
        )

        task_id = progress.add_task(f"Downloading: {title[:30]}...", total=None)

        def progress_hook(d: Dict[str, Any]) -> None:
            if d['status'] == 'downloading':
                total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
                downloaded = d.get('downloaded_bytes', 0)
                
                if total > 0:
                    progress.update(task_id, total=total, completed=downloaded)
                else:
                    # If total is unknown, just update downloaded amount
                    progress.update(task_id, completed=downloaded)

            elif d['status'] == 'finished':
                progress.update(task_id, description="[bold green]Processing (FFmpeg)...", total=100, completed=100)
                # Store the final filepath
                if 'filename' in d:
                    result["filepath"] = d['filename']

        ydl_opts['progress_hooks'] = [progress_hook]

        try:
            with progress:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    error_code = ydl.download([url])
                    if error_code == 0:
                        result["success"] = True
                    else:
                        result["error"] = f"yt-dlp exited with code {error_code}"
        except yt_dlp.utils.DownloadError as e:
            result["error"] = str(e)
            logger.error(f"DownloadError: {e}")
        except Exception as e:
            result["error"] = str(e)
            logger.exception("Unexpected error during download")

        return result

    def download_video(self, url: str, quality: str, custom_format_id: Optional[str] = None) -> Dict[str, Any]:
        """Prepares and executes a video download."""
        output_dir = Path(config.get("default_video_folder"))
        output_template = str(output_dir / config.get("filename_template"))
        
        ydl_opts = self.base_opts.copy()
        ydl_opts['outtmpl'] = output_template
        ydl_opts['postprocessors'] = self._get_postprocessors("video")
        
        # Determine format string
        if custom_format_id:
            format_str = f"{custom_format_id}+bestaudio/best"
        elif quality == "Best":
            format_str = "bestvideo+bestaudio/best"
        else:
            height = quality.replace('p', '')
            format_str = f"bestvideo[height<={height}]+bestaudio/bestvideo[height<={height}]/best"
            
        ydl_opts['format'] = format_str

        # Fetch title for progress bar
        info = self.extract_info(url)
        title = info.get('title', 'Unknown Video') if info else 'Video'

        logger.info(f"Starting video download: {url} | Quality: {quality}")
        return self._download_with_progress(url, ydl_opts, title)

    def download_audio(self, url: str, audio_format: str, bitrate: str) -> Dict[str, Any]:
        """Prepares and executes an audio download."""
        output_dir = Path(config.get("default_audio_folder"))
        output_template = str(output_dir / config.get("filename_template"))
        
        ydl_opts = self.base_opts.copy()
        ydl_opts['outtmpl'] = output_template
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = self._get_postprocessors("audio", audio_format, bitrate)

        # Fetch title for progress bar
        info = self.extract_info(url)
        title = info.get('title', 'Unknown Audio') if info else 'Audio'

        logger.info(f"Starting audio download: {url} | Format: {audio_format} | Bitrate: {bitrate}")
        return self._download_with_progress(url, ydl_opts, title)

# Singleton instance to be imported
downloader = Downloader()
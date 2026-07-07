import json
from datetime import datetime
from typing import Any
from satube.config import HISTORY_FILE
from satube.logger import logger

class HistoryManager:
    """Manages the download history, saving records to a local JSON file."""

    def __init__(self) -> None:
        self.history: list[dict[str, Any]] = []
        self.load()

    def load(self) -> None:
        """Loads the download history from the JSON file."""
        if HISTORY_FILE.exists():
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    self.history = json.load(f)
            except (json.JSONDecodeError, OSError) as e:
                logger.error(f"Failed to load history file: {e}")
                self.history = []
        else:
            self.history = []

    def save(self) -> None:
        """Saves the current history list to the JSON file."""
        try:
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(self.history, f, indent=4)
        except OSError as e:
            logger.error(f"Failed to save history file: {e}")

    def add_entry(self, title: str, media_type: str, location: str, file_size: str) -> None:
        """
        Adds a new successful download record to the history.
        
        Args:
            title: The title of the downloaded media.
            media_type: 'Video' or 'Audio' (or 'Playlist').
            location: The absolute file path where it was saved.
            file_size: Human-readable string of the file size.
        """
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "title": title,
            "type": media_type,
            "location": location,
            "size": file_size
        }
        self.history.append(entry)
        self.save()

    def get_all(self) -> list[dict[str, Any]]:
        """Returns all history records, newest first."""
        return list(reversed(self.history))

    def search(self, query: str) -> list[dict[str, Any]]:
        """
        Searches the history by title, type, or location.
        Returns records matching the query, newest first.
        """
        query_lower = query.lower()
        results = [
            entry for entry in self.history
            if query_lower in entry.get("title", "").lower() or
               query_lower in entry.get("type", "").lower() or
               query_lower in entry.get("location", "").lower()
        ]
        return list(reversed(results))

    def delete_entry(self, index: int) -> bool:
        """
        Deletes a specific history entry based on its current index.
        Note: The index should correspond to the chronological list.
        """
        try:
            # We must account for the fact that the UI usually displays reversed history
            # So, if an index is passed based on the normal list, remove it.
            del self.history[index]
            self.save()
            return True
        except IndexError:
            logger.error(f"Attempted to delete invalid history index: {index}")
            return False

    def clear(self) -> None:
        """Clears all download history."""
        self.history.clear()
        self.save()

# Singleton instance to be imported across the application
history_manager = HistoryManager()
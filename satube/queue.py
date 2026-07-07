from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
from satube.logger import logger

class QueueStatus(Enum):
    """Represents the current state of an item in the download queue."""
    PENDING = "Pending"
    DOWNLOADING = "Downloading..."
    COMPLETED = "Completed"
    FAILED = "Failed"
    SKIPPED = "Skipped"

@dataclass
class QueueItem:
    """Represents a single media item in the download queue."""
    url: str
    status: QueueStatus = QueueStatus.PENDING
    title: str = "Fetching..."  # Updated once metadata is retrieved
    media_type: str = "video"   # 'video' or 'audio'

class QueueManager:
    """Manages the list of URLs queued for sequential downloading."""

    def __init__(self) -> None:
        self.items: List[QueueItem] = []

    def add(self, url: str, media_type: str = "video") -> None:
        """Adds a new URL to the end of the queue."""
        self.items.append(QueueItem(url=url, media_type=media_type))
        logger.info(f"Added to queue: {url} as {media_type}")

    def remove(self, index: int) -> bool:
        """
        Removes an item from the queue based on a 1-based index (UI friendly).
        Returns True if successful, False if the index is out of bounds.
        """
        if 1 <= index <= len(self.items):
            removed_item = self.items.pop(index - 1)
            logger.info(f"Removed from queue: {removed_item.url}")
            return True
        logger.warning(f"Failed to remove queue item at index {index}: Out of bounds.")
        return False

    def move(self, old_index: int, new_index: int) -> bool:
        """
        Moves an item from one 1-based index to another.
        Returns True if successful, False if indices are invalid.
        """
        if 1 <= old_index <= len(self.items) and 1 <= new_index <= len(self.items):
            # Convert to 0-based indices
            item = self.items.pop(old_index - 1)
            self.items.insert(new_index - 1, item)
            logger.info(f"Moved queue item from {old_index} to {new_index}")
            return True
        logger.warning(f"Failed to move queue item from {old_index} to {new_index}: Out of bounds.")
        return False

    def clear(self) -> None:
        """Removes all items from the queue."""
        self.items.clear()
        logger.info("Cleared the download queue.")

    def get_all(self) -> List[QueueItem]:
        """Returns the entire list of queued items."""
        return self.items

    def get_next_pending(self) -> Optional[QueueItem]:
        """Returns the next item marked as PENDING, or None if the queue is empty/finished."""
        for item in self.items:
            if item.status == QueueStatus.PENDING:
                return item
        return None

    def has_pending(self) -> bool:
        """Checks if there are any pending items left in the queue."""
        return any(item.status == QueueStatus.PENDING for item in self.items)
        
    def count_pending(self) -> int:
        """Returns the total number of pending items."""
        return sum(1 for item in self.items if item.status == QueueStatus.PENDING)

# Singleton instance to be imported across the application
queue_manager = QueueManager()
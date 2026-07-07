import json
from pathlib import Path
from typing import Any
from platformdirs import user_config_dir, user_data_dir

APP_NAME = "satube"

# Define standard Linux directories
CONFIG_DIR = Path(user_config_dir(APP_NAME))
DATA_DIR = Path(user_data_dir(APP_NAME))
CONFIG_FILE = CONFIG_DIR / "config.json"
HISTORY_FILE = DATA_DIR / "history.json"
LOG_DIR = DATA_DIR / "logs"

DEFAULT_CONFIG = {
    "default_video_folder": str(Path.home() / "Downloads" / "SATube" / "Videos"),
    "default_audio_folder": str(Path.home() / "Downloads" / "SATube" / "Audio"),
    "default_quality": "1080p",
    "default_audio_format": "MP3",
    "theme": "Auto",
    "concurrent_downloads": 3,
    "filename_template": "%(title)s.%(ext)s",
    "embed_thumbnail": True,
    "embed_metadata": True,
    "notifications_enabled": True,
    "ask_before_overwrite": True,
    "resume_downloads": True,
    "remember_previous": True,
    "previous_quality": "1080p",
    "previous_audio_format": "MP3"
}

class ConfigManager:
    """Manages application configuration, persisting settings to a JSON file."""
    
    def __init__(self) -> None:
        self.config: dict[str, Any] = DEFAULT_CONFIG.copy()
        self.ensure_dirs()
        self.load()

    def ensure_dirs(self) -> None:
        """Create necessary application directories if they do not exist."""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        
        # Ensure default download directories exist based on current config
        Path(self.config["default_video_folder"]).mkdir(parents=True, exist_ok=True)
        Path(self.config["default_audio_folder"]).mkdir(parents=True, exist_ok=True)

    def load(self) -> None:
        """Load settings from the JSON configuration file."""
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    user_config = json.load(f)
                    # Update config with user settings, keeping new defaults if keys are missing
                    self.config.update(user_config)
            except (json.JSONDecodeError, OSError):
                # If the file is corrupted or unreadable, overwrite it safely on next save
                pass

    def save(self) -> None:
        """Save the current settings to the JSON configuration file."""
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4)
        except OSError as e:
            # We will handle logging later, but for now we print to terminal
            print(f"Warning: Could not save configuration file: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a configuration value."""
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Update a configuration value and save it to disk."""
        self.config[key] = value
        self.save()

# Singleton instance to be imported across the application
config = ConfigManager()
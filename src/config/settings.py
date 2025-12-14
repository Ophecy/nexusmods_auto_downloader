"""
Application-wide settings and constants.
"""


class Settings:
    """Global application settings."""
    
    # Nexus Mods
    NEXUS_BASE_URL = "https://www.nexusmods.com"
    
    # Batch processing
    BATCH_SIZE = 50
    
    # Default delays (seconds)
    DEFAULT_DELAY_BEFORE_CLICK = 2.0
    DEFAULT_DELAY_FOR_DOWNLOAD = 6.0
    DEFAULT_DELAY_BETWEEN_MODS = 0.5
    
    # Default files
    DEFAULT_COLLECTION_FILE = "collection.json"
    DEFAULT_PROGRESS_FILE = "downloaded_mods.txt"
    
    # Default game
    DEFAULT_GAME_DOMAIN = "cyberpunk2077"

    # Template matching
    DEFAULT_TEMPLATE_PATH = "templates/slow_download_button.png"
    DEFAULT_DETECTION_CONFIDENCE = 0.8
    DEFAULT_TEMPLATE_WIDTH = 200
    DEFAULT_TEMPLATE_HEIGHT = 100

    # Browser reopening delay after batch close
    BROWSER_REOPEN_DELAY = 5.0

    # Tab close delay
    TAB_CLOSE_DELAY = 0.3

"""
Domain model for downloader configuration.
"""

from dataclasses import dataclass


@dataclass
class DownloaderConfig:
    """Configuration for the downloader."""

    game_domain: str = "cyberpunk2077"
    delay_before_click: float = 2.0
    delay_for_download: float = 6.0
    delay_between_mods: float = 0.5
    auto_close: bool = True
    progress_file: str = "downloaded_mods.txt"
    force_focus: bool = False
    batch_size: int = 50
    use_auto_detection: bool = False
    template_path: str = "templates/slow_download_button.png"
    detection_confidence: float = 0.8

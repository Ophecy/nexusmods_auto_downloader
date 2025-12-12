"""
Infrastructure layer: Technical implementations.
Contains adapters to external systems (file system, browser, input devices).
"""

from src.infrastructure.persistence.collection_reader import CollectionReader
from src.infrastructure.persistence.progress_tracker import ProgressTracker
from src.infrastructure.browser.browser_controller import BrowserController
from src.infrastructure.input.click_recorder import ClickRecorder

__all__ = [
    "CollectionReader",
    "ProgressTracker",
    "BrowserController",
    "ClickRecorder",
]

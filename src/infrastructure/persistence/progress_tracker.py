"""
Progress tracking implementation for crash recovery.
"""

from pathlib import Path
from typing import Set

from src.domain.mod_source import ModSource


class ProgressTracker:
    """Manages download progress and crash recovery."""
    
    def __init__(self, progress_file: str):
        """
        Initialize the progress tracker.
        
        Args:
            progress_file: Path to the progress tracking file
        """
        self.progress_file = Path(progress_file)
        self.downloaded_mods: Set[str] = self._load_progress()
    
    def _load_progress(self) -> Set[str]:
        """
        Load previously downloaded mods from file.
        
        Returns:
            Set of mod keys that were previously downloaded
        """
        if not self.progress_file.exists():
            return set()
        
        with open(self.progress_file, 'r') as f:
            return set(line.strip() for line in f if line.strip())
    
    def is_downloaded(self, mod_source: ModSource) -> bool:
        """
        Check if a mod was already downloaded.
        
        Args:
            mod_source: The mod to check
            
        Returns:
            True if mod was already downloaded, False otherwise
        """
        mod_key = mod_source.to_key()
        return mod_key in self.downloaded_mods
    
    def mark_downloaded(self, mod_source: ModSource):
        """
        Mark a mod as downloaded.
        
        Args:
            mod_source: The mod to mark as downloaded
        """
        mod_key = mod_source.to_key()
        self.downloaded_mods.add(mod_key)
        
        with open(self.progress_file, 'a') as f:
            f.write(f"{mod_key}\n")
    
    def get_stats(self, total: int) -> tuple:
        """
        Get download statistics.
        
        Args:
            total: Total number of mods in collection
            
        Returns:
            Tuple of (downloaded_count, remaining_count)
        """
        downloaded = len(self.downloaded_mods)
        remaining = total - downloaded
        return downloaded, remaining

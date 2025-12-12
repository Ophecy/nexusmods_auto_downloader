"""
URL builder for Nexus Mods downloads.
"""

from src.domain.mod_source import ModSource
from src.config.settings import Settings


class NexusUrlBuilder:
    """Builds Nexus Mods download URLs."""
    
    def __init__(self, game_domain: str):
        """
        Initialize the URL builder.
        
        Args:
            game_domain: Game identifier on Nexus Mods (e.g., 'cyberpunk2077')
        """
        self.game_domain = game_domain
    
    def build_download_url(self, mod_source: ModSource) -> str:
        """
        Build download URL for a mod.
        
        Args:
            mod_source: The mod to build URL for
            
        Returns:
            Complete download URL
        """
        return (
            f"{Settings.NEXUS_BASE_URL}/{self.game_domain}/mods/"
            f"{mod_source.mod_id}?tab=files"
            f"&file_id={mod_source.file_id}&nmm=1"
        )

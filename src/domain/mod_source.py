"""
Domain model for mod identification.
"""

from dataclasses import dataclass


@dataclass
class ModSource:
    """Represents a mod's identification on Nexus Mods."""
    
    mod_id: int
    file_id: int
    
    def to_key(self) -> str:
        """
        Generate a unique key for this mod.
        
        Returns:
            String key in format "mod_id:file_id"
        """
        return f"{self.mod_id}:{self.file_id}"
    
    @staticmethod
    def from_key(key: str) -> "ModSource":
        """
        Create ModSource from a key string.
        
        Args:
            key: String in format "mod_id:file_id"
            
        Returns:
            ModSource instance
        """
        mod_id, file_id = key.split(":")
        return ModSource(mod_id=int(mod_id), file_id=int(file_id))

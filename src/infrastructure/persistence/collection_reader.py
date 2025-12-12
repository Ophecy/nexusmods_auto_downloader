"""
Collection file reader implementation.
"""

import json
from pathlib import Path
from typing import List

from src.domain.mod_source import ModSource


class CollectionReader:
    """Reads mod collection from JSON file."""
    
    def __init__(self, file_path: Path):
        """
        Initialize the collection reader.
        
        Args:
            file_path: Path to the collection JSON file
        """
        self.file_path = file_path
    
    def read_mods(self) -> List[ModSource]:
        """
        Parse collection file and extract mod sources.
        
        Returns:
            List of ModSource objects
            
        Raises:
            FileNotFoundError: If collection file doesn't exist
            json.JSONDecodeError: If file is not valid JSON
        """
        with open(self.file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        return [
            self._extract_mod_source(mod)
            for mod in data.get('mods', [])
        ]
    
    @staticmethod
    def _extract_mod_source(mod: dict) -> ModSource:
        """
        Extract mod ID and file ID from mod data.
        
        Args:
            mod: Dictionary containing mod information
            
        Returns:
            ModSource instance
        """
        source = mod.get('source', {})
        return ModSource(
            mod_id=source.get('modId'),
            file_id=source.get('fileId')
        )

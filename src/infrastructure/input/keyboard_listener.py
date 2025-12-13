"""
Keyboard listener for emergency stop functionality.
"""

import sys
from pynput import keyboard


class KeyboardListener:
    """Listens for keyboard events to provide emergency stop functionality."""
    
    def __init__(self, stop_key=keyboard.Key.f4):
        """
        Initialize the keyboard listener.
        
        Args:
            stop_key: The key that triggers emergency stop (default: F4)
        """
        self.stop_key = stop_key
        self.should_stop = False
        self.listener = None
    
    def start(self):
        """Start listening for keyboard events in background."""
        self.listener = keyboard.Listener(on_press=self._on_press)
        self.listener.start()
    
    def stop(self):
        """Stop listening for keyboard events."""
        if self.listener:
            self.listener.stop()
    
    def _on_press(self, key):
        """
        Handle key press events.
        
        Args:
            key: The key that was pressed
        """
        if key == self.stop_key:
            print("\n\n[EMERGENCY STOP] F4 pressed - stopping script...")
            self.should_stop = True
            return False
    
    def check_should_stop(self) -> bool:
        """
        Check if stop was requested.
        
        Returns:
            True if stop was requested, False otherwise
        """
        return self.should_stop

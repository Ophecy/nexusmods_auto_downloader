"""
User click recording implementation using pynput.
"""

from typing import Optional
from pynput import mouse


class ClickRecorder:
    """Records user's manual click position."""
    
    def __init__(self):
        """Initialize the click recorder."""
        self.click_position: Optional[tuple] = None
    
    def record_click(self) -> Optional[tuple]:
        """
        Wait for and record a mouse click.
        
        Returns:
            Tuple of (x, y) coordinates if click was recorded, None otherwise
        """
        print("\n" + "="*60)
        print("CLICK RECORDING")
        print("="*60)
        print("First page will open...")
        print("CLICK on the 'SLOW DOWNLOAD' button")
        print("Your coordinates will be recorded.")
        print("="*60 + "\n")
        
        def on_click(x, y, button, pressed):
            if pressed and button == mouse.Button.left:
                self.click_position = (x, y)
                print(f"\nClick recorded at: ({x}, {y})")
                return False
        
        with mouse.Listener(on_click=on_click) as listener:
            listener.join()
        
        return self.click_position

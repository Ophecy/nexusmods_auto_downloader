"""
Browser automation implementation using pyautogui.
"""

import time
import pyautogui

from src.config.settings import Settings


class BrowserController:
    """Controls browser tabs using keyboard shortcuts."""
    
    @staticmethod
    def close_current_tab():
        """Close the currently active tab."""
        pyautogui.hotkey('ctrl', 'w')
        time.sleep(Settings.TAB_CLOSE_DELAY)
    
    @staticmethod
    def close_all_tabs():
        """Close all browser tabs."""
        pyautogui.hotkey('ctrl', 'shift', 'w')
        time.sleep(1)
    
    @staticmethod
    def close_tabs_batch(count: int):
        """
        Close multiple tabs one by one.

        Args:
            count: Number of tabs to close
        """
        for _ in range(count):
            pyautogui.hotkey('ctrl', 'w')
            time.sleep(0.1)

    @staticmethod
    def focus_browser():
        """Bring browser to foreground by opening and closing a dummy tab."""
        import webbrowser
        webbrowser.open("https://www.nexusmods.com")
        time.sleep(0.1)
        BrowserController.close_current_tab()

"""
Main orchestration service for automated downloads.
"""

import time
import webbrowser
import pyautogui
from pathlib import Path
from typing import Optional

from src.domain.mod_source import ModSource
from src.domain.downloader_config import DownloaderConfig
from src.infrastructure.persistence.collection_reader import CollectionReader
from src.infrastructure.persistence.progress_tracker import ProgressTracker
from src.infrastructure.browser.browser_controller import BrowserController
from src.infrastructure.input.click_recorder import ClickRecorder
from src.infrastructure.input.keyboard_listener import KeyboardListener
from src.services.url_builder import NexusUrlBuilder
from src.config.settings import Settings


class DownloadOrchestrator:
    """Main orchestrator for automated downloads."""
    
    def __init__(self, collection_file: Path, config: DownloaderConfig):
        """
        Initialize the download orchestrator.
        
        Args:
            collection_file: Path to collection JSON file
            config: Downloader configuration
        """
        self.reader = CollectionReader(collection_file)
        self.url_builder = NexusUrlBuilder(config.game_domain)
        self.config = config
        self.recorder = ClickRecorder()
        self.browser = BrowserController()
        self.tracker = ProgressTracker(config.progress_file)
        self.keyboard_listener = KeyboardListener()
        self.click_position: Optional[tuple] = None
    
    def execute(self):
        """Execute the download automation."""
        self.keyboard_listener.start()
        print("Press F4 at any time to stop the script\n")
        
        all_mods = self.reader.read_mods()
        total = len(all_mods)
        
        if total == 0:
            print("No mods found in collection file")
            return
        
        mod_sources = [
            mod for mod in all_mods 
            if not self.tracker.is_downloaded(mod)
        ]
        
        downloaded, remaining = self.tracker.get_stats(total)
        
        self._print_header(total, downloaded, remaining)
        
        if remaining == 0:
            print("All mods already downloaded!")
            return
        
        first_mod = mod_sources[0]
        if not self._record_first_click(first_mod):
            return
        
        self.tracker.mark_downloaded(first_mod)
        
        print("\n" + "="*60)
        print("Starting automatic downloads...")
        print("="*60 + "\n")
        
        for idx, source in enumerate(mod_sources[1:], start=2):
            if self.keyboard_listener.check_should_stop():
                print("\nStopping as requested...")
                break
            
            self._process_mod(source, idx + downloaded, total)
            self.tracker.mark_downloaded(source)
            
            if not self.config.auto_close and idx % Settings.BATCH_SIZE == 0:
                self._close_all_tabs_batch()
        
        if not self.config.auto_close and len(mod_sources) > 1:
            self._close_all_tabs_batch()
        
        self.keyboard_listener.stop()
        print(f"\nAll downloads initiated!")
        print(f"\nProgress file: {self.config.progress_file}")
    
    def _print_header(self, total: int, downloaded: int, remaining: int):
        """Print status header."""
        print(f"\n{'='*60}")
        print(f"Nexus Auto-Downloader")
        print(f"{'='*60}")
        print(f"Total mods: {total}")
        print(f"Already downloaded: {downloaded}")
        print(f"Remaining: {remaining}")
        print(f"{'='*60}\n")
    
    def _record_first_click(self, mod_source: ModSource) -> bool:
        """Record user's click on the first mod."""
        print(f"[1/...] First mod")
        print(f"Mod ID: {mod_source.mod_id}, File ID: {mod_source.file_id}\n")
        
        url = self.url_builder.build_download_url(mod_source)
        webbrowser.open(url)
        
        print("Waiting for page to load...")
        time.sleep(self.config.delay_before_click)
        
        self.click_position = self.recorder.record_click()
        
        if not self.click_position:
            print("No click recorded")
            return False
        
        print("\nClosing tab...")
        self.browser.close_current_tab()
        time.sleep(1)
        
        return True
    
    def _close_all_tabs_batch(self):
        """Close all accumulated tabs and restart browser."""
        print("\n" + "="*60)
        print("PAUSE - Closing accumulated tabs")
        print("="*60)
        print("Waiting for downloads to start...")
        time.sleep(self.config.delay_for_download)
        
        print("Closing all tabs (Ctrl+W for each)...")
        self.browser.close_tabs_batch(Settings.BATCH_SIZE)
        
        print("Reopening browser...")
        time.sleep(1)
        webbrowser.open(Settings.NEXUS_BASE_URL)
        
        print(f"Waiting for browser to be ready ({Settings.BROWSER_REOPEN_DELAY}s)...")
        time.sleep(Settings.BROWSER_REOPEN_DELAY)
        
        print("Browser ready, resuming...\n")
    
    def _process_mod(self, mod_source: ModSource, index: int, total: int):
        """Process a single mod download."""
        if self.keyboard_listener.check_should_stop():
            return
        
        print(f"[{index}/{total}] Mod {mod_source.mod_id} "
              f"(File {mod_source.file_id})")
        
        url = self.url_builder.build_download_url(mod_source)
        webbrowser.open(url)
        
        if self.keyboard_listener.check_should_stop():
            return
        
        print(f"  Loading...")
        time.sleep(self.config.delay_before_click)
        
        if self.keyboard_listener.check_should_stop():
            return
        
        print(f"  Clicking at {self.click_position}")
        x, y = self.click_position
        pyautogui.click(x, y)
        
        if self.config.auto_close:
            time.sleep(self.config.delay_for_download)
            self.browser.close_current_tab()
        
        time.sleep(self.config.delay_between_mods)

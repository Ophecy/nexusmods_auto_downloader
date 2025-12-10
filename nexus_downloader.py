"""
Nexus Mods Auto-Downloader
Automates mod downloads from Nexus Mods with click recording and crash recovery.
"""

import json
import webbrowser
import time
import pyautogui
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional, Set
from pynput import mouse


@dataclass
class ModSource:
    """Represents a mod's identification."""
    mod_id: int
    file_id: int


@dataclass
class DownloaderConfig:
    """Configuration for the downloader."""
    game_domain: str = "cyberpunk2077"
    delay_before_click: float = 2.0
    delay_for_download: float = 6.0
    delay_between_mods: float = 0.5
    auto_close: bool = True
    progress_file: str = "downloaded_mods.txt"


class ProgressTracker:
    """Manages download progress and crash recovery."""
    
    def __init__(self, progress_file: str):
        self.progress_file = Path(progress_file)
        self.downloaded_mods: Set[str] = self._load_progress()

    def _load_progress(self) -> Set[str]:
        """Load previously downloaded mods from file."""
        if not self.progress_file.exists():
            return set()
        
        with open(self.progress_file, 'r') as f:
            return set(line.strip() for line in f if line.strip())

    def is_downloaded(self, mod_source: ModSource) -> bool:
        """Check if a mod was already downloaded."""
        mod_key = f"{mod_source.mod_id}:{mod_source.file_id}"
        return mod_key in self.downloaded_mods

    def mark_downloaded(self, mod_source: ModSource):
        """Mark a mod as downloaded."""
        mod_key = f"{mod_source.mod_id}:{mod_source.file_id}"
        self.downloaded_mods.add(mod_key)
        
        with open(self.progress_file, 'a') as f:
            f.write(f"{mod_key}\n")

    def get_stats(self, total: int) -> tuple:
        """Get download statistics."""
        downloaded = len(self.downloaded_mods)
        remaining = total - downloaded
        return downloaded, remaining


class ClickRecorder:
    """Records user's manual click position."""
    
    def __init__(self):
        self.click_position = None

    def record_click(self) -> Optional[tuple]:
        """Wait for and record a mouse click."""
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
                print(f"\n✓ Click recorded at: ({x}, {y})")
                return False
        
        with mouse.Listener(on_click=on_click) as listener:
            listener.join()
        
        return self.click_position


class CollectionReader:
    """Reads mod collection from JSON file."""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path

    def read_mods(self) -> List[ModSource]:
        """Parse collection file and extract mod sources."""
        with open(self.file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        return [
            self._extract_mod_source(mod)
            for mod in data.get('mods', [])
        ]

    @staticmethod
    def _extract_mod_source(mod: dict) -> ModSource:
        """Extract mod ID and file ID from mod data."""
        source = mod.get('source', {})
        return ModSource(
            mod_id=source.get('modId'),
            file_id=source.get('fileId')
        )


class NexusUrlBuilder:
    """Builds Nexus Mods download URLs."""
    
    BASE_URL = "https://www.nexusmods.com"

    def __init__(self, game_domain: str):
        self.game_domain = game_domain

    def build_download_url(self, mod_source: ModSource) -> str:
        """Build download URL for a mod."""
        return (
            f"{self.BASE_URL}/{self.game_domain}/mods/"
            f"{mod_source.mod_id}?tab=files"
            f"&file_id={mod_source.file_id}&nmm=1"
        )


class BrowserController:
    """Controls browser tabs."""
    
    @staticmethod
    def close_current_tab():
        """Close the currently active tab."""
        pyautogui.hotkey('ctrl', 'w')
        time.sleep(0.3)

    @staticmethod
    def close_all_tabs():
        """Close all browser tabs."""
        pyautogui.hotkey('ctrl', 'shift', 'w')
        time.sleep(1)


class NexusAutoDownloader:
    """Main orchestrator for automated downloads."""
    
    BATCH_SIZE = 50  # Close tabs every N mods in no-auto-close mode

    def __init__(self, collection_file: Path, config: DownloaderConfig):
        self.reader = CollectionReader(collection_file)
        self.url_builder = NexusUrlBuilder(config.game_domain)
        self.config = config
        self.recorder = ClickRecorder()
        self.browser = BrowserController()
        self.tracker = ProgressTracker(config.progress_file)
        self.click_position = None

    def execute(self):
        """Execute the download automation."""
        all_mods = self.reader.read_mods()
        total = len(all_mods)
        
        if total == 0:
            print("❌ No mods found in collection file")
            return
        
        # Filter out already downloaded mods
        mod_sources = [
            mod for mod in all_mods 
            if not self.tracker.is_downloaded(mod)
        ]
        
        downloaded, remaining = self.tracker.get_stats(total)
        
        self._print_header(total, downloaded, remaining)
        
        if remaining == 0:
            print("✓ All mods already downloaded!")
            return
        
        # Record click position from first mod
        first_mod = mod_sources[0]
        if not self._record_first_click(first_mod):
            return
        
        self.tracker.mark_downloaded(first_mod)
        
        print("\n" + "="*60)
        print("Starting automatic downloads...")
        print("="*60 + "\n")
        
        # Process remaining mods
        for idx, source in enumerate(mod_sources[1:], start=2):
            self._process_mod(source, idx + downloaded, total)
            self.tracker.mark_downloaded(source)
            
            # Close tabs in batches when in no-auto-close mode
            if not self.config.auto_close and idx % self.BATCH_SIZE == 0:
                self._close_all_tabs_batch()
        
        # Final cleanup for remaining tabs
        if not self.config.auto_close and len(mod_sources) > 1:
            self._close_all_tabs_batch()
        
        print(f"\n✓ All downloads initiated!")
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
            print("❌ No click recorded")
            return False
        
        print("\nClosing tab...")
        self.browser.close_current_tab()
        time.sleep(1)
        
        return True

    def _close_all_tabs_batch(self):
        """Close all accumulated tabs and restart browser."""
        print("\n" + "="*60)
        print("⏸️  PAUSE - Closing accumulated tabs")
        print("="*60)
        print("Waiting for downloads to start...")
        time.sleep(self.config.delay_for_download)
        
        print("Closing all tabs (Ctrl+Shift+W)...")
        self.browser.close_all_tabs()
        
        print("Reopening browser...")
        webbrowser.open('about:blank')
        
        print("Waiting for browser restart (10s)...")
        time.sleep(10)
        
        print("✓ Browser ready, resuming...\n")

    def _process_mod(self, mod_source: ModSource, index: int, total: int):
        """Process a single mod download."""
        print(f"[{index}/{total}] Mod {mod_source.mod_id} "
              f"(File {mod_source.file_id})")
        
        # Open mod page
        url = self.url_builder.build_download_url(mod_source)
        webbrowser.open(url)
        
        # Wait for page load
        print(f"  Loading...")
        time.sleep(self.config.delay_before_click)
        
        # Click at recorded position
        print(f"  Clicking at {self.click_position}")
        x, y = self.click_position
        pyautogui.click(x, y)
        
        # Close tab if in auto-close mode
        if self.config.auto_close:
            time.sleep(self.config.delay_for_download)
            self.browser.close_current_tab()
        
        time.sleep(self.config.delay_between_mods)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Nexus Mods Auto-Downloader - Automate mod downloads from Nexus Mods",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python nexus_downloader.py
  python nexus_downloader.py --no-auto-close
  python nexus_downloader.py --collection my_mods.json
  python nexus_downloader.py --delay-click 3 --delay-download 8
  python nexus_downloader.py --reset-progress
        """
    )
    
    parser.add_argument(
        '--collection',
        default='collection.json',
        help='Collection JSON file (default: collection.json)'
    )
    
    parser.add_argument(
        '--no-auto-close',
        action='store_true',
        help='Keep tabs open (batch close every 50 mods)'
    )
    
    parser.add_argument(
        '--progress-file',
        default='downloaded_mods.txt',
        help='Progress tracking file (default: downloaded_mods.txt)'
    )
    
    parser.add_argument(
        '--reset-progress',
        action='store_true',
        help='Reset progress file'
    )
    
    parser.add_argument(
        '--delay-click',
        type=float,
        default=2.0,
        help='Delay before clicking in seconds (default: 2.0)'
    )
    
    parser.add_argument(
        '--delay-download',
        type=float,
        default=6.0,
        help='Wait time for download start in seconds (default: 6.0)'
    )
    
    parser.add_argument(
        '--delay-between',
        type=float,
        default=0.5,
        help='Delay between mods in seconds (default: 0.5)'
    )
    
    parser.add_argument(
        '--game',
        default='cyberpunk2077',
        help='Game domain on Nexus Mods (default: cyberpunk2077)'
    )
    
    parser.add_argument(
        '--yes', '-y',
        action='store_true',
        help='Skip confirmation prompt'
    )
    
    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_args()
    
    collection_file = Path(args.collection)
    
    if not collection_file.exists():
        print(f"❌ Error: {collection_file} not found")
        return
    
    # Handle progress reset
    if args.reset_progress:
        progress_file = Path(args.progress_file)
        if progress_file.exists():
            progress_file.unlink()
            print(f"✓ Progress file deleted: {progress_file}")
        else:
            print(f"ℹ️ No progress file to delete")
        return
    
    # Print instructions
    print("\n" + "="*60)
    print("NEXUS AUTO-DOWNLOADER")
    print("="*60)
    print()
    print("How it works:")
    print("  1. First page opens")
    print("  2. YOU click on 'SLOW DOWNLOAD' button")
    print("  3. Your coordinates are recorded")
    print("  4. Script automatically clicks at same position")
    print("     on all following pages")
    print()
    print("Configuration:")
    print(f"  • Collection: {args.collection}")
    print(f"  • Progress: {args.progress_file}")
    print(f"  • Click delay: {args.delay_click}s")
    
    if not args.no_auto_close:
        print(f"  • Auto-close: Yes (waits {args.delay_download}s before closing)")
        print(f"    ➝ Waits for download to start before closing tab")
    else:
        print(f"  • Auto-close: No (batch of 50)")
        print(f"    ➝ Tabs stay open then closed every 50 mods")
        print(f"    ➝ Faster but opens up to 50 tabs")
    
    print()
    print("Make sure:")
    print("  ✓ You are logged in to Nexus Mods")
    print("  ✓ Your browser is in fullscreen")
    print("  ✓ You don't move the window during process")
    print("="*60)
    print()
    
    if not args.yes:
        input("Press ENTER to continue...")
    
    # Create configuration
    config = DownloaderConfig(
        game_domain=args.game,
        delay_before_click=args.delay_click,
        delay_for_download=args.delay_download,
        delay_between_mods=args.delay_between,
        auto_close=not args.no_auto_close,
        progress_file=args.progress_file
    )
    
    # Run downloader
    try:
        downloader = NexusAutoDownloader(collection_file, config)
        downloader.execute()
    except KeyboardInterrupt:
        print("\n\n[STOP] Stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()

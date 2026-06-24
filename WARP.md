# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview
Nexus Mods Auto-Downloader is a Python automation tool that uses GUI automation (pyautogui, pynput) to automate mod downloads from Nexus Mods. It records a user's manual click on the first mod's download button, then replicates that click on all subsequent mods in a collection.

**Key Constraint**: This tool relies on GUI automation with absolute screen coordinates. Any changes must preserve the click recording and replay mechanism.

## Development Commands

### Setup
```powershell
# Create virtual environment and install dependencies
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Running the Application
```powershell
# Standard mode (safe, closes tabs automatically)
python nexus_downloader.py

# Fast mode (3x faster, keeps up to 50 tabs open)
python nexus_downloader.py --no-auto-close

# Different game
python nexus_downloader.py --game skyrimspecialedition

# Custom delays for slower connections
python nexus_downloader.py --delay-click 3 --delay-download 10

# Reset progress and start fresh
python nexus_downloader.py --reset-progress

# See all options
python nexus_downloader.py --help
```

### Testing
There is currently no test suite. When adding tests:
- Test with small collections (5-10 mods) first
- Mock pyautogui and webbrowser for unit tests
- Integration tests require a real browser and Nexus account

## Architecture

### Core Design Pattern
The codebase follows **SOLID principles** with clear separation of concerns. Each class has a single responsibility and functions are kept under 30 lines.

### Component Flow
```
main() → NexusAutoDownloader.execute()
    ↓
    1. CollectionReader → Parse collection.json
    2. ProgressTracker → Filter already-downloaded mods
    3. ClickRecorder → Record user's click on first mod
    4. For each remaining mod:
        - NexusUrlBuilder → Generate download URL
        - BrowserController → Open tab and click
        - ProgressTracker → Mark as downloaded
```

### Key Components

**NexusAutoDownloader** (Orchestrator)
- Main coordinator that sequences all operations
- Implements batch closing logic (every 50 mods in fast mode)
- Handles crash recovery by using ProgressTracker

**ProgressTracker** (Crash Recovery)
- Maintains `downloaded_mods.txt` with format: `{modId}:{fileId}`
- Loads progress on startup to skip already-downloaded mods
- Appends to file immediately after each download (crash-safe)

**ClickRecorder** (User Input Capture)
- Uses pynput mouse listener to capture a single left-click
- Stores coordinates as tuple (x, y)
- **Critical**: These coordinates are absolute screen positions, not relative to window

**CollectionReader** (JSON Parser)
- Reads Nexus Mods collection.json format
- Extracts only `modId` and `fileId` from `source` object
- Returns list of ModSource dataclasses

**NexusUrlBuilder** (URL Generation)
- Constructs Nexus Mods download URLs with format:
  `https://www.nexusmods.com/{game}/mods/{modId}?tab=files&file_id={fileId}&nmm=1`
- The `nmm=1` parameter triggers the download flow

**BrowserController** (Browser Automation)
- Uses pyautogui hotkeys for tab management
- `Ctrl+W` to close current tab
- `Ctrl+Shift+W` to close all tabs (fast mode batch cleanup)

### Data Model
**ModSource** dataclass holds:
- `mod_id`: Nexus mod identifier
- `file_id`: Specific file version identifier

**DownloaderConfig** dataclass holds all timing and behavior settings.

## Important Constraints

### GUI Automation Limitations
- Browser window must remain visible (not minimized)
- Browser window cannot move during execution
- Click coordinates are absolute screen positions
- Multi-monitor setups may require adjustment
- The tool assumes fullscreen browser for consistency

### Timing Parameters
- `delay_before_click`: Wait for page load before clicking (default: 2s)
- `delay_for_download`: Wait for download to start before closing tab (default: 6s)
- `delay_between_mods`: Throttle between opening tabs (default: 0.5s)

These must be tuned based on:
- Internet connection speed
- Nexus server response time
- Computer performance
- Free vs. Premium Nexus account

### Fast Mode Batch Processing
- Opens up to 50 tabs before closing (BATCH_SIZE constant)
- Waits 10 seconds after closing all tabs to restart browser
- This is 3x faster but memory-intensive

### Progress File Format
`downloaded_mods.txt` uses simple format: `modId:fileId` per line
- No headers, no JSON
- Duplicates are ignored via Set
- File is append-only (never modified, only extended)

## Collection File Format
Uses official Nexus Mods collection format. Only required fields:
```json
{
  "mods": [
    {
      "source": {
        "modId": 123456,
        "fileId": 789012
      }
    }
  ]
}
```
All other fields (name, version, author, etc.) are ignored.

## Typical Modifications

### Changing Timing Behavior
Modify DownloaderConfig defaults in the dataclass or command-line parsing.

### Supporting New Browser Shortcuts
Modify BrowserController hotkey combinations. Note: Windows/Linux use Ctrl, macOS uses Cmd.

### Adjusting Batch Size
Change `NexusAutoDownloader.BATCH_SIZE` constant (currently 50).

### Adding Logging
All print statements could be replaced with proper logging. Keep crash recovery (ProgressTracker) file writes separate from logs.

## Known Limitations
- Requires user to be logged in to Nexus Mods
- Does not verify downloads actually succeeded
- Assumes "SLOW DOWNLOAD" button is in same position for all mods
- No support for Premium fast download paths
- May violate Nexus Mods Terms of Service (use at own risk)

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python-based automation tool for downloading mods from Nexus Mods using browser automation. Records user clicks once, then automatically downloads hundreds of mods with crash recovery support.

## Essential Commands

### Running the Application
```bash
# Standard run (current working directory must be project root)
python -m src.main

# With options (fast mode example)
python -m src.main --no-auto-close --delay-click 1 --delay-download 4

# See all options
python -m src.main --help
```

**IMPORTANT**: Always use `python -m src.main`, NOT `python src/main.py` or the deprecated `nexus_downloader.py`.

### Development Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Dependencies: pyautogui, pynput, Pillow
```

### Testing
Currently no test suite exists. See ARCHITECTURE.md for planned test structure.

## Architecture Overview

This project follows **Layered Architecture** with strict unidirectional dependencies:

```
Presentation → Services → Infrastructure → Domain
                             ↓
                        Configuration
```

### Layer Structure

**Domain Layer** (`src/domain/`)
- Pure business models with zero external dependencies
- `ModSource`: Mod identification (mod_id, file_id)
- `DownloaderConfig`: Configuration data structure
- `exceptions.py`: Custom domain exceptions

**Infrastructure Layer** (`src/infrastructure/`)
- Adapters to external systems
- `persistence/`: File I/O (CollectionReader, ProgressTracker)
- `browser/`: Browser automation via pyautogui (BrowserController)
- `input/`: User input capture (ClickRecorder, KeyboardListener)

**Services Layer** (`src/services/`)
- Business logic orchestration
- `DownloadOrchestrator`: Main workflow coordinator
- `NexusUrlBuilder`: URL construction logic

**Presentation Layer** (`src/presentation/`)
- User interface and interaction
- `cli/`: Command-line interface (argument_parser, command_handler)
- `console/`: Console output formatting

**Configuration Layer** (`src/config/`)
- `Settings`: Global constants (URLs, delays, batch sizes, default files)

### Key Architectural Rules

1. **One class per file** - Each component is in its own file
2. **Dependencies flow downward only** - Lower layers never import from higher layers
3. **No business logic in presentation** - Delegate to Services layer
4. **Infrastructure is swappable** - E.g., can replace pyautogui with Selenium

## Critical Implementation Details

### Progress Tracking
Progress is persisted to `downloaded_mods.txt` (configurable) in format:
```
mod_id:file_id
123456:789012
```

The `ProgressTracker` (src/infrastructure/persistence/progress_tracker.py) automatically skips already-downloaded mods on restart, enabling crash recovery.

### Emergency Stop
The `KeyboardListener` (src/infrastructure/input/keyboard_listener.py) monitors for **F4 key press** to immediately halt execution. This listener runs in the background throughout the entire download process.

### Click Recording Workflow
1. Opens first mod URL in browser
2. `ClickRecorder` captures user's single click on "SLOW DOWNLOAD" button
3. Coordinates are stored and reused for all subsequent mods
4. Browser automation via `BrowserController` using pyautogui

### Batch Processing
When `--no-auto-close` is enabled:
- Opens up to 50 tabs (configurable via `Settings.BATCH_SIZE`)
- Downloads all mods in the batch
- Closes all tabs at once
- Repeat for next batch
- Much faster than standard mode (3x speedup)

### URL Construction
`NexusUrlBuilder` (src/services/url_builder.py) builds URLs in format:
```
https://www.nexusmods.com/{game}/mods/{mod_id}?tab=files&file_id={file_id}
```

Default game domain is `cyberpunk2077` (configurable via `--game` flag).

## Modifying This Codebase

### Adding New Features

**For new UI elements**: Add to `src/presentation/`
- CLI additions → `presentation/cli/`
- Console formatting → `presentation/console/`
- Future GUI → Create `presentation/gui/`

**For new business logic**: Add to `src/services/`
- Must coordinate infrastructure components
- Can depend on Domain and Infrastructure layers

**For new integrations**: Add to `src/infrastructure/`
- E.g., Nexus API client → `infrastructure/api/nexus_api_client.py`
- E.g., Selenium browser → `infrastructure/browser/selenium_controller.py`

**For new data models**: Add to `src/domain/`
- Keep pure (no external library dependencies)
- Use dataclasses for simple DTOs

### Configuration Changes

All configurable constants live in `src/config/settings.py`:
- Default delays
- Batch sizes
- Default file paths
- Nexus Mods base URL

To change defaults, modify `Settings` class, not hardcoded values elsewhere.

### Dependency Injection Pattern

Services receive dependencies via constructor:
```python
class DownloadOrchestrator:
    def __init__(self, collection_file: Path, config: DownloaderConfig):
        self.reader = CollectionReader(collection_file)
        self.tracker = ProgressTracker(config.progress_file)
        # ...
```

This enables easy testing with mocks and swappable implementations.

## Important Constraints

1. **Browser must remain visible** - pyautogui requires window to be on screen
2. **Browser position must not change** - Click coordinates are absolute screen positions
3. **User must be logged in to Nexus Mods** - Downloads require authentication
4. **Collection file format** - Must match Nexus Mods export format (see collection_example.json)

## Future Extensions (Planned)

See IMPROVEMENTS.md and README.md "Future Features" section for detailed roadmap:
- GUI implementation (PyQt5/Tkinter)
- Automatic button detection (OCR)
- Nexus Premium API support
- Selenium integration for headless mode
- Enhanced error handling and retry logic
- YAML configuration persistence

When implementing these, maintain layered architecture:
- New browser automation → Add to `infrastructure/browser/`
- New API client → Add to `infrastructure/api/`
- New GUI → Add to `presentation/gui/`

## Constraints while developping
- Only structural comment, no explanatory comment.

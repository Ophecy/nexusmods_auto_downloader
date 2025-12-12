# Architecture Documentation

## Overview

This project follows a **Layered Architecture** (also known as N-Tier Architecture) with clear separation of concerns. The architecture promotes maintainability, testability, and scalability.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                  Presentation Layer                     │
│  (CLI, Console Output, User Interaction)                │
│                                                         │
│  • argument_parser.py - Command-line arguments          │
│  • command_handler.py - Main application logic          │
│  • formatter.py - Console output formatting             │
└────────────────────────────┬────────────────────────────┘
                             |
                             ↓
┌─────────────────────────────────────────────────────────┐
│                    Services Layer                       │
│         (Business Logic & Orchestration)                │
│                                                         │
│  • download_orchestrator.py - Main download logic       │
│  • url_builder.py - URL construction                    │
└────────────────────────────┬────────────────────────────┘
                             |
                             ↓
┌─────────────────────────────────────────────────────────┐
│                 Infrastructure Layer                    │
│      (External System Adapters & Technical)             │
│                                                         │
│  Persistence:                                           │
│  • collection_reader.py - JSON file reading             │
│  • progress_tracker.py - Progress persistence           │
│                                                         │
│  Browser:                                               │
│  • browser_controller.py - Browser automation           │
│                                                         │
│  Input:                                                 │
│  • click_recorder.py - User input capture               │
└────────────────────────────┬────────────────────────────┘
                             |
                             ↓
┌─────────────────────────────────────────────────────────┐
│                     Domain Layer                        │
│          (Pure Business Models & Rules)                 │
│                                                         │
│  • mod_source.py - Mod identification model             │
│  • downloader_config.py - Configuration model           │
│  • exceptions.py - Domain exceptions                    │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                    Configuration                        │
│                                                         │
│  • settings.py - Global constants and defaults          │
└─────────────────────────────────────────────────────────┘
```

## Layer Responsibilities

### 1. Domain Layer (`src/domain/`)

**Purpose**: Contains pure business logic and models. No external dependencies.

**Components**:
- `ModSource`: Represents a mod's unique identification (mod_id, file_id)
- `DownloaderConfig`: Configuration data for the downloader
- `exceptions.py`: Custom domain exceptions

**Rules**:
- No imports from other layers
- No external library dependencies (except dataclasses from stdlib)
- Pure data structures and business rules

**Example**:
```python
from src.domain.mod_source import ModSource

mod = ModSource(mod_id=12345, file_id=67890)
key = mod.to_key()  # "12345:67890"
```

### 2. Infrastructure Layer (`src/infrastructure/`)

**Purpose**: Technical implementations and adapters to external systems.

**Sub-packages**:

#### Persistence (`infrastructure/persistence/`)
- `CollectionReader`: Reads mod collections from JSON files
- `ProgressTracker`: Manages download progress persistence

#### Browser (`infrastructure/browser/`)
- `BrowserController`: Controls browser tabs using pyautogui

#### Input (`infrastructure/input/`)
- `ClickRecorder`: Captures user mouse clicks using pynput

**Rules**:
- Can depend on Domain layer
- Cannot depend on Services or Presentation layers
- Implements adapters for external libraries
- Handles I/O operations

**Example**:
```python
from src.infrastructure.persistence.progress_tracker import ProgressTracker

tracker = ProgressTracker("downloaded_mods.txt")
if not tracker.is_downloaded(mod_source):
    # Download the mod
    tracker.mark_downloaded(mod_source)
```

### 3. Services Layer (`src/services/`)

**Purpose**: Business logic orchestration and coordination.

**Components**:
- `DownloadOrchestrator`: Main service coordinating the download process
- `NexusUrlBuilder`: Constructs Nexus Mods URLs

**Rules**:
- Can depend on Domain and Infrastructure layers
- Cannot depend on Presentation layer
- Implements use cases and workflows
- Orchestrates multiple infrastructure components

**Example**:
```python
from src.services.download_orchestrator import DownloadOrchestrator

orchestrator = DownloadOrchestrator(collection_file, config)
orchestrator.execute()
```

### 4. Presentation Layer (`src/presentation/`)

**Purpose**: User interface and interaction.

**Sub-packages**:

#### CLI (`presentation/cli/`)
- `argument_parser.py`: Parses command-line arguments
- `command_handler.py`: Main application entry point

#### Console (`presentation/console/`)
- `formatter.py`: Formats console output

**Rules**:
- Can depend on all other layers
- Handles user input and output
- No business logic (delegates to Services)

**Example**:
```python
from src.presentation.cli.command_handler import main

main()  # Runs the application
```

### 5. Configuration Layer (`src/config/`)

**Purpose**: Application-wide settings and constants.

**Components**:
- `Settings`: Global constants (URLs, delays, batch sizes, etc.)

**Rules**:
- No dependencies on other layers
- Only contains static configuration
- Can be imported by any layer

**Example**:
```python
from src.config.settings import Settings

print(Settings.NEXUS_BASE_URL)  # "https://www.nexusmods.com"
```

## Dependency Flow

```
Presentation → Services → Infrastructure → Domain
                              ↓
                         Configuration
```

**Key Principle**: Dependencies only flow downward. Lower layers never import from higher layers.

## File Organization

```
src/
├── __init__.py
├── main.py                              # Entry point
│
├── domain/                              # Pure business models
│   ├── __init__.py
│   ├── mod_source.py
│   ├── downloader_config.py
│   └── exceptions.py
│
├── infrastructure/                      # Technical implementations
│   ├── __init__.py
│   ├── persistence/
│   │   ├── __init__.py
│   │   ├── collection_reader.py
│   │   └── progress_tracker.py
│   ├── browser/
│   │   ├── __init__.py
│   │   └── browser_controller.py
│   └── input/
│       ├── __init__.py
│       └── click_recorder.py
│
├── services/                            # Business logic
│   ├── __init__.py
│   ├── url_builder.py
│   └── download_orchestrator.py
│
├── presentation/                        # User interface
│   ├── __init__.py
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── argument_parser.py
│   │   └── command_handler.py
│   └── console/
│       ├── __init__.py
│       └── formatter.py
│
└── config/                              # Configuration
    ├── __init__.py
    └── settings.py
```

## Design Patterns Used

### 1. Layered Architecture
Separation into Domain, Infrastructure, Services, and Presentation layers.

### 2. Dependency Injection
Services receive dependencies through constructor parameters:
```python
class DownloadOrchestrator:
    def __init__(self, collection_file: Path, config: DownloaderConfig):
        self.reader = CollectionReader(collection_file)
        self.tracker = ProgressTracker(config.progress_file)
        # ...
```

### 3. Data Transfer Objects (DTOs)
`ModSource` and `DownloaderConfig` are simple data containers.

### 4. Facade Pattern
`DownloadOrchestrator` provides a simple interface to complex subsystems.

### 5. Strategy Pattern (Future)
Different download strategies can be implemented (e.g., Premium API vs. browser automation).

## Testing Strategy

### Unit Tests
- **Domain Layer**: Test business logic without external dependencies
- **Infrastructure Layer**: Mock file system and external libraries
- **Services Layer**: Mock infrastructure components
- **Presentation Layer**: Mock services

### Integration Tests
- Test complete workflows end-to-end
- Use test fixtures for collection files

### Test Structure
```
tests/
├── unit/
│   ├── domain/
│   │   └── test_mod_source.py
│   ├── infrastructure/
│   │   ├── test_collection_reader.py
│   │   └── test_progress_tracker.py
│   └── services/
│       └── test_download_orchestrator.py
├── integration/
│   └── test_full_workflow.py
└── fixtures/
    └── test_collection.json
```

## Future Extensions

### GUI Implementation
Add a new presentation layer without touching existing code:
```
src/presentation/gui/
├── __init__.py
├── main_window.py
├── progress_widget.py
└── settings_dialog.py
```

### API Client for Premium Users
Add new infrastructure adapter:
```
src/infrastructure/api/
├── __init__.py
└── nexus_api_client.py
```

### Selenium Browser Automation
Replace pyautogui implementation:
```
src/infrastructure/browser/
├── __init__.py
├── browser_controller.py          # Abstract interface
├── pyautogui_controller.py        # Current implementation
└── selenium_controller.py         # New implementation
```

## Benefits of This Architecture

1. **Maintainability**: Each component has a single responsibility
2. **Testability**: Easy to mock dependencies and test in isolation
3. **Scalability**: New features can be added without modifying existing code
4. **Flexibility**: Easy to swap implementations (e.g., pyautogui → Selenium)
5. **Clarity**: Clear separation makes code easy to understand
6. **Reusability**: Domain and Service layers can be reused in different UIs

## Migration from Old Structure

The original monolithic `nexus_downloader.py` has been refactored into:

| Original Class | New Location |
|---------------|--------------|
| `ModSource` | `src/domain/mod_source.py` |
| `DownloaderConfig` | `src/domain/downloader_config.py` |
| `ProgressTracker` | `src/infrastructure/persistence/progress_tracker.py` |
| `ClickRecorder` | `src/infrastructure/input/click_recorder.py` |
| `CollectionReader` | `src/infrastructure/persistence/collection_reader.py` |
| `NexusUrlBuilder` | `src/services/url_builder.py` |
| `BrowserController` | `src/infrastructure/browser/browser_controller.py` |
| `NexusAutoDownloader` | `src/services/download_orchestrator.py` |
| `parse_args()` | `src/presentation/cli/argument_parser.py` |
| `main()` | `src/presentation/cli/command_handler.py` |

## Running the Application

### Old Way
```bash
python nexus_downloader.py --no-auto-close
```

### New Way
```bash
python -m src.main --no-auto-close
# or
cd src && python main.py --no-auto-close
```

## Conclusion

This layered architecture provides a solid foundation for future growth while maintaining clean, testable, and maintainable code. Each layer has clear responsibilities and dependencies flow in one direction, making the system easy to understand and extend.

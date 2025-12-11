# Immediate Improvements Roadmap

This document outlines actionable improvements to implement in the short term, prioritized by impact and ease of implementation.

---

## 🚀 Priority 1: Critical Fixes & Quick Wins

### 1. Fix Tab Management Bug
**Issue**: Currently closes exactly `BATCH_SIZE` (50) tabs even if fewer tabs are open.
**Impact**: High - Can cause errors
**Effort**: Low (30 minutes)

**Current code:**
```python
for i in range(self.BATCH_SIZE):
    pyautogui.hotkey('ctrl', 'w')
```

**Solution**: Track actual number of opened tabs and close only those.

```python
class NexusAutoDownloader:
    def __init__(self, ...):
        self.open_tabs_count = 0
    
    def _process_mod(self, ...):
        self.open_tabs_count += 1
        # ... existing code
    
    def _close_all_tabs_batch(self):
        print(f"Closing {self.open_tabs_count} tabs...")
        for i in range(self.open_tabs_count):
            pyautogui.hotkey('ctrl', 'w')
            time.sleep(0.1)
        self.open_tabs_count = 0
```

---

### 2. Add Dry-Run Mode
**Impact**: High - Test without downloading
**Effort**: Low (1 hour)

**Implementation**:
```python
# In DownloaderConfig
@dataclass
class DownloaderConfig:
    # ... existing fields
    dry_run: bool = False

# In parse_args()
parser.add_argument(
    '--dry-run',
    action='store_true',
    help='Simulate downloads without actually clicking'
)

# In _process_mod()
def _process_mod(self, mod_source: ModSource, index: int, total: int):
    print(f"[{index}/{total}] Mod {mod_source.mod_id} (File {mod_source.file_id})")
    
    url = self.url_builder.build_download_url(mod_source)
    
    if self.config.dry_run:
        print(f"  [DRY-RUN] Would open: {url}")
        print(f"  [DRY-RUN] Would click at {self.click_position}")
        time.sleep(0.1)  # Minimal delay for readability
        return
    
    # ... existing code
```

---

### 3. Enhanced Logging System
**Impact**: High - Better debugging
**Effort**: Medium (2-3 hours)

**Implementation**:
```python
import logging
from logging.handlers import RotatingFileHandler

# Add to main()
def setup_logging(verbose: bool = False):
    """Setup logging with file rotation."""
    log_level = logging.DEBUG if verbose else logging.INFO
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        'nexus_downloader.log',
        maxBytes=5*1024*1024,  # 5MB
        backupCount=3
    )
    file_handler.setLevel(logging.DEBUG)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    
    # Format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Setup root logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# Add --verbose flag
parser.add_argument(
    '--verbose', '-v',
    action='store_true',
    help='Enable verbose logging'
)

# Use throughout code
logger = logging.getLogger(__name__)
logger.info(f"Processing mod {mod_id}")
logger.debug(f"Opening URL: {url}")
logger.error(f"Failed to process mod: {error}")
```

---

### 4. YAML Configuration File
**Impact**: High - Persistent settings
**Effort**: Medium (2-3 hours)

**Implementation**:
```python
import yaml

# config.yaml structure
"""
default:
  game_domain: cyberpunk2077
  delay_before_click: 2.0
  delay_for_download: 6.0
  delay_between_mods: 0.5
  auto_close: true

click_positions:
  cyberpunk2077: [1920, 540]
  skyrimspecialedition: [1920, 540]

presets:
  fast:
    delay_before_click: 1.0
    delay_for_download: 4.0
    auto_close: false
  
  slow:
    delay_before_click: 3.0
    delay_for_download: 10.0
"""

class ConfigManager:
    """Manages configuration loading and saving."""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            return self._default_config()
        
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _default_config(self) -> dict:
        """Return default configuration."""
        return {
            'default': {
                'game_domain': 'cyberpunk2077',
                'delay_before_click': 2.0,
                'delay_for_download': 6.0,
                'delay_between_mods': 0.5,
                'auto_close': True
            },
            'click_positions': {},
            'presets': {}
        }
    
    def save_click_position(self, game: str, position: tuple):
        """Save click position for a game."""
        if 'click_positions' not in self.config:
            self.config['click_positions'] = {}
        
        self.config['click_positions'][game] = list(position)
        self._save_config()
    
    def get_click_position(self, game: str) -> Optional[tuple]:
        """Get saved click position for a game."""
        pos = self.config.get('click_positions', {}).get(game)
        return tuple(pos) if pos else None
    
    def _save_config(self):
        """Save configuration to file."""
        with open(self.config_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)

# Add to requirements.txt
# pyyaml
```

---

### 5. Collection Validation
**Impact**: Medium - Prevent errors
**Effort**: Low (1 hour)

**Implementation**:
```python
class CollectionReader:
    def validate_collection(self) -> tuple[bool, list[str]]:
        """Validate collection file structure."""
        errors = []
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except json.JSONDecodeError as e:
            return False, [f"Invalid JSON: {e}"]
        
        if 'mods' not in data:
            errors.append("Missing 'mods' key in collection")
            return False, errors
        
        if not isinstance(data['mods'], list):
            errors.append("'mods' must be an array")
            return False, errors
        
        for idx, mod in enumerate(data['mods']):
            if 'source' not in mod:
                errors.append(f"Mod #{idx}: missing 'source'")
            else:
                source = mod['source']
                if 'modId' not in source:
                    errors.append(f"Mod #{idx}: missing 'modId'")
                if 'fileId' not in source:
                    errors.append(f"Mod #{idx}: missing 'fileId'")
        
        return len(errors) == 0, errors
    
    def read_mods(self) -> List[ModSource]:
        """Parse collection file with validation."""
        valid, errors = self.validate_collection()
        
        if not valid:
            print("⚠️ Collection validation errors:")
            for error in errors:
                print(f"  - {error}")
            
            if not input("\nContinue anyway? (y/n): ").lower() == 'y':
                return []
        
        # ... existing code
```

---

## 🔧 Priority 2: Reliability Improvements

### 6. Smart Retry System
**Impact**: High - Handle transient failures
**Effort**: Medium (3-4 hours)

**Implementation**:
```python
import time
from functools import wraps

def retry_with_backoff(max_attempts=3, base_delay=2):
    """Decorator for retry logic with exponential backoff."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    
                    delay = base_delay * (2 ** attempt)
                    logger.warning(
                        f"Attempt {attempt + 1} failed: {e}. "
                        f"Retrying in {delay}s..."
                    )
                    time.sleep(delay)
        return wrapper
    return decorator

# Usage
@retry_with_backoff(max_attempts=3, base_delay=2)
def _process_mod(self, mod_source: ModSource, index: int, total: int):
    # ... existing code
```

---

### 7. Enhanced Progress Tracker (JSON)
**Impact**: High - Better metadata
**Effort**: Medium (2-3 hours)

**Implementation**:
```python
import json
from datetime import datetime

class EnhancedProgressTracker:
    """Enhanced progress tracking with metadata."""
    
    def __init__(self, progress_file: str):
        self.progress_file = Path(progress_file).with_suffix('.json')
        self.data = self._load_progress()
    
    def _load_progress(self) -> dict:
        """Load progress from JSON file."""
        if not self.progress_file.exists():
            return {}
        
        with open(self.progress_file, 'r') as f:
            return json.load(f)
    
    def is_downloaded(self, mod_source: ModSource) -> bool:
        """Check if mod was downloaded."""
        mod_key = f"{mod_source.mod_id}:{mod_source.file_id}"
        entry = self.data.get(mod_key, {})
        return entry.get('status') == 'completed'
    
    def mark_downloaded(self, mod_source: ModSource, success: bool = True):
        """Mark mod with metadata."""
        mod_key = f"{mod_source.mod_id}:{mod_source.file_id}"
        
        if mod_key not in self.data:
            self.data[mod_key] = {'attempts': 0}
        
        self.data[mod_key].update({
            'status': 'completed' if success else 'failed',
            'last_attempt': datetime.now().isoformat(),
            'attempts': self.data[mod_key].get('attempts', 0) + 1
        })
        
        self._save_progress()
    
    def _save_progress(self):
        """Save progress to JSON file."""
        with open(self.progress_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def get_stats(self, total: int) -> dict:
        """Get detailed statistics."""
        completed = sum(1 for v in self.data.values() 
                       if v.get('status') == 'completed')
        failed = sum(1 for v in self.data.values() 
                    if v.get('status') == 'failed')
        
        return {
            'total': total,
            'completed': completed,
            'failed': failed,
            'remaining': total - completed - failed
        }
```

---

### 8. Error Screenshots
**Impact**: Medium - Better debugging
**Effort**: Low (1 hour)

**Implementation**:
```python
from PIL import ImageGrab
from datetime import datetime

class ErrorHandler:
    """Handles errors with screenshots."""
    
    def __init__(self, screenshot_dir: str = "error_screenshots"):
        self.screenshot_dir = Path(screenshot_dir)
        self.screenshot_dir.mkdir(exist_ok=True)
    
    def capture_error(self, mod_source: ModSource, error: Exception):
        """Capture screenshot and log error."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"error_{mod_source.mod_id}_{timestamp}.png"
        filepath = self.screenshot_dir / filename
        
        try:
            screenshot = ImageGrab.grab()
            screenshot.save(filepath)
            logger.error(
                f"Error processing mod {mod_source.mod_id}: {error}. "
                f"Screenshot saved: {filepath}"
            )
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")

# Add to requirements.txt
# pillow

# Usage in _process_mod
try:
    # ... existing code
except Exception as e:
    self.error_handler.capture_error(mod_source, e)
    raise
```

---

## 📊 Priority 3: User Experience

### 9. Better Progress Display
**Impact**: Medium - User feedback
**Effort**: Low (1 hour)

**Implementation**:
```python
def _print_progress(self, current: int, total: int, mod_source: ModSource):
    """Print formatted progress bar."""
    percentage = (current / total) * 100
    bar_length = 40
    filled = int(bar_length * current / total)
    bar = '█' * filled + '░' * (bar_length - filled)
    
    print(f"\r[{bar}] {percentage:.1f}% ({current}/{total}) | "
          f"Mod {mod_source.mod_id}", end='', flush=True)
```

---

### 10. Keyboard Interrupt Handler
**Impact**: Low - Clean shutdown
**Effort**: Low (30 minutes)

**Implementation**:
```python
import signal
import sys

class GracefulShutdown:
    """Handle graceful shutdown on Ctrl+C."""
    
    def __init__(self, downloader):
        self.downloader = downloader
        self.shutdown = False
        signal.signal(signal.SIGINT, self._signal_handler)
    
    def _signal_handler(self, sig, frame):
        """Handle shutdown signal."""
        if self.shutdown:
            print("\n\n[FORCE STOP] Forcing shutdown...")
            sys.exit(1)
        
        print("\n\n[PAUSE] Finishing current download...")
        print("Press Ctrl+C again to force quit")
        self.shutdown = True

# Usage in main()
shutdown_handler = GracefulShutdown(downloader)
```

---

## 📝 Implementation Checklist

### Week 1
- [ ] Fix tab management bug
- [ ] Add dry-run mode
- [ ] Implement basic logging
- [ ] Add collection validation

### Week 2
- [ ] Setup YAML configuration
- [ ] Implement retry system
- [ ] Enhanced progress tracker (JSON)
- [ ] Add error screenshots

### Week 3
- [ ] Better progress display
- [ ] Graceful shutdown handler
- [ ] Write tests for new features
- [ ] Update documentation

---

## 🧪 Testing Recommendations

For each improvement:
1. **Unit tests**: Test individual functions
2. **Integration tests**: Test with small collection (5 mods)
3. **Stress tests**: Test with large collection (100+ mods)
4. **Error tests**: Simulate failures and verify recovery

---

## 📦 Additional Dependencies

Add to `requirements.txt`:
```
pyyaml>=6.0
pillow>=10.0
```

---

## 🔄 Migration Notes

### Progress File Migration
If implementing JSON progress tracker, provide migration:

```python
def migrate_progress_file(old_file: str, new_file: str):
    """Migrate from TXT to JSON format."""
    if not Path(old_file).exists():
        return
    
    data = {}
    with open(old_file, 'r') as f:
        for line in f:
            mod_key = line.strip()
            if mod_key:
                data[mod_key] = {
                    'status': 'completed',
                    'migrated': True
                }
    
    with open(new_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✓ Migrated {len(data)} entries to {new_file}")
```

---

**Estimated Total Implementation Time**: 2-3 weeks for all Priority 1 & 2 improvements.

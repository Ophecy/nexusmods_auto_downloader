# Nexus Mods Auto-Downloader

🚀 Automate mod downloads from Nexus Mods with intelligent click recording and crash recovery.

## ✨ Features

- 🎯 **One-Click Learning**: Click once, auto-download hundreds of mods
- 🤖 **Smart Auto-Detection**: Automatic button detection with dual-template matching (normal + hover states)
- 🔄 **Crash Recovery**: Automatically resume from where you left off
- ⚡ **Batch Processing**: Fast mode handles up to 50 tabs at once
- 🎮 **Multi-Game Support**: Works with any game on Nexus Mods
- ⚙️ **Highly Configurable**: Adjust all delays and behaviors
- 📊 **Progress Tracking**: Never lose track of downloaded mods
- 🏗️ **Clean Architecture**: SOLID principles, well-documented code

## 🎥 How It Works

### Standard Mode (Coordinate-Based)
1. Run the script
2. First page opens automatically
3. **You click** on the "SLOW DOWNLOAD" button
4. Script records your click coordinates
5. All subsequent mods download automatically!

### Auto-Detection Mode (Recommended)
1. Place button templates in `templates/` folder
2. Run with `--auto-detect` flag
3. Script automatically finds and clicks the button
4. Works even if button position changes!

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/yourusername/nexus-auto-downloader.git
cd nexus-auto-downloader
pip install -r requirements.txt
```

### Basic Usage

```bash
python -m src.main
```

That's it! The script will guide you through the process.

**Note**: The old `nexus_downloader.py` is deprecated. Use `python -m src.main` instead.

## 📖 Examples

### Standard Mode
```bash
python -m src.main
```
Safe and reliable, closes each tab after download.

### Fast Mode (3x faster!)
```bash
python -m src.main --no-auto-close
```
Opens up to 50 tabs, then closes them in batch. Much faster!

### Different Game (Skyrim)
```bash
python -m src.main --game skyrimspecialedition
```

### Custom Collection
```bash
python -m src.main --collection my_mods.json
```

### Optimized for Fast Connection
```bash
python -m src.main --delay-click 1 --delay-download 4
```

### Resume After Crash
```bash
python -m src.main
```
Automatically skips already downloaded mods!

### Force Browser Focus
```bash
python -m src.main --force-focus
```
Forces browser to foreground before each click. Use if other windows appear on top.

### Auto-Detection Mode
```bash
python -m src.main --auto-detect
```
Automatically detects the "SLOW DOWNLOAD" button using template matching. Requires button templates in `templates/` folder.

## 🎛️ All Options

```bash
python -m src.main --help
```

| Option                  | Default                          | Description                              |
|-------------------------|----------------------------------|------------------------------------------|
| `--collection`          | `collection.json`                | Collection file to use                   |
| `--progress-file`       | `downloaded_mods.txt`            | Progress tracking file                   |
| `--no-auto-close`       | `False`                          | Fast mode (batch close every 50)         |
| `--reset-progress`      | -                                | Clear progress file                      |
| `--delay-click`         | `2.0`                            | Delay before clicking (seconds)          |
| `--delay-download`      | `6.0`                            | Wait for download start (seconds)        |
| `--delay-between`       | `0.5`                            | Delay between mods (seconds)             |
| `--game`                | `cyberpunk2077`                  | Game domain on Nexus Mods                |
| `--force-focus`         | `False`                          | Force browser focus before clicks        |
| `--batch-size`          | `100`                            | Tabs per batch in fast mode              |
| `--auto-detect`         | `False`                          | Enable automatic button detection        |
| `--template-path`       | `templates/slow_download_button.png` | Path to button template image        |
| `--detection-confidence`| `0.8`                            | Confidence threshold for detection (0-1) |
| `-y, --yes`             | `False`                          | Skip confirmation prompt                 |

## 📊 Performance

| Mode                     | Speed     | 300 Mods |
|--------------------------|-----------|----------|
| Standard                 | ~8.5s/mod | ~42 min  |
| Fast (`--no-auto-close`) | ~2.5s/mod | ~14 min  |

**Fast mode is 3x faster!** ⚡

## 🎮 Supported Games

Works with **any game** on Nexus Mods!

Examples: `cyberpunk2077`, `skyrimspecialedition`, `fallout4`, `witcher3`, `starfield`, `newvegas`, and many more.

Just use the domain from the URL: `nexusmods.com/{game-domain}/mods/...`

## 🤖 Auto-Detection Setup

The auto-detection feature uses template matching to automatically find and click the "SLOW DOWNLOAD" button.

### Setting Up Templates

1. **Capture button screenshots**:
   - Navigate to any Nexus Mods download page
   - Take a screenshot of the "SLOW DOWNLOAD" button in **normal state** (not hovered)
   - Hover over the button and take another screenshot in **hover state**

2. **Prepare template images**:
   - Crop both screenshots to show only the button (approximately 200x100 pixels)
   - Save as PNG files in the `templates/` folder:
     - `slow_download_button.png` (normal state)
     - `slow_download_button_hover.png` (hover state)

3. **Run with auto-detection**:
   ```bash
   python -m src.main --auto-detect
   ```

### Template Requirements

- Both templates must exist for auto-detection to work
- Use the same button state for all templates (don't mix different pages)
- Templates are automatically protected from being overwritten
- Works across different screen resolutions

### Adjusting Detection Sensitivity

If the button is not detected reliably:

```bash
# Lower confidence threshold (0.7 = 70% match required)
python -m src.main --auto-detect --detection-confidence 0.7

# Higher confidence (0.9 = 90% match required)
python -m src.main --auto-detect --detection-confidence 0.9
```

**Tip**: Start with 0.8 (default) and lower it to 0.7 if detection fails.

## 📁 Collection File

Your `collection.json` should follow the Nexus Mods format:

```json
{
  "mods": [
    {
      "name": "Mod Name",
      "source": {
        "modId": 123456,
        "fileId": 789012
      }
    }
  ]
}
```

See `collection_example.json` for a complete example.

## 🔄 Crash Recovery

Progress is automatically saved to `downloaded_mods.txt`:

```
123456:789012
234567:890123
```

If the script crashes, just rerun it - it will skip already downloaded mods!

To start fresh:
```bash
python -m src.main --reset-progress
```

## ⚙️ Optimal Settings

### Fast Connection + SSD
```bash
python -m src.main --delay-click 1 --delay-download 4 --no-auto-close
```

### Normal Connection (Recommended)
```bash
python -m src.main
```

### Slow Connection
```bash
python -m src.main --delay-click 3 --delay-download 10
```

## 🛠️ Troubleshooting

**No click recorded?**
- Make sure page has fully loaded
- Click directly on "SLOW DOWNLOAD" button

**Wrong click location?**
- Keep browser in fullscreen
- Don't move window during process
- Increase `--delay-click` if page loads slowly
- Consider using `--auto-detect` for automatic detection

**Downloads not starting?**
- Increase `--delay-download` to 8 or 10
- Check you're logged in to Nexus Mods

**Clicks missing the target?**
- Use `--force-focus` to bring browser to foreground before each click
- Other windows (notifications, popups) might be appearing on top
- Ensure browser stays visible and not minimized
- Use `--auto-detect` for automatic button location

**Auto-detection not working?**
- Ensure both template files exist in `templates/`:
  - `slow_download_button.png` (normal state)
  - `slow_download_button_hover.png` (hover state)
- Lower `--detection-confidence` to 0.7 if button not detected
- Check templates were captured from the correct button state

## ⚠️ Important

- You must be **logged in** to Nexus Mods
- Keep **browser window visible** (not minimized)
- Don't **move the browser** during the process
- **Press F4 at any time** to stop the script immediately
- Automation may violate Nexus Mods ToS - use at your own risk

## 🏗️ Architecture

Refactored with clean **Layered Architecture** and SOLID principles:

### Layers
- **Domain**: Pure business models (`ModSource`, `DownloaderConfig`)
- **Infrastructure**: Technical adapters (file system, browser, input)
- **Services**: Business logic orchestration (`DownloadOrchestrator`)
- **Presentation**: CLI interface and console output
- **Config**: Application settings and constants

### Key Components
- **DownloadOrchestrator**: Main service coordinating downloads
- **ProgressTracker**: Progress management & crash recovery
- **ClickRecorder**: Records user's manual click
- **ButtonDetector**: Automatic button detection with dual-template matching
- **CollectionReader**: Parses collection JSON
- **NexusUrlBuilder**: Builds download URLs
- **BrowserController**: Browser automation

**One file per class**, fully documented with clear dependencies.

See `ARCHITECTURE.md` for detailed documentation.

## 🤝 Contributing

Contributions welcome! Feel free to submit a Pull Request.

## 📄 License

**CC BY-NC 4.0** (Creative Commons Attribution-NonCommercial 4.0 International)

- ✅ **Free to use** for personal and non-commercial purposes
- ✅ **Free to modify** and adapt
- ✅ **Free to share** with attribution
- ❌ **Commercial use** requires explicit written permission

For commercial inquiries, please contact the author.

See [LICENSE](LICENSE) file for full details.

## 💡 Tips

1. **Use auto-detection** (`--auto-detect`) for better reliability if button position changes
2. Test with a small collection first (5-10 mods)
3. Use `--no-auto-close` for large collections (much faster)
4. Combine auto-detection with fast mode: `--auto-detect --no-auto-close`
5. Check your browser's download settings
6. Consider a Nexus Premium account for faster downloads

## 🔮 Future Features

### Planned Features

#### User Experience
- 🖥️ **Graphical Interface (GUI)**: PyQt5/Tkinter interface with real-time progress visualization
- ✅ ~~**Automatic Button Detection**~~: **IMPLEMENTED** - Dual-template matching (normal + hover states)
- 🔔 **Notifications**: Desktop notifications, Discord webhooks, and email alerts
- ⏸️ **Pause/Resume**: Keyboard shortcuts to pause and resume downloads
- 🧪 **Dry-Run Mode**: Preview what would be downloaded without actually downloading

#### Reliability & Error Handling
- 🔄 **Smart Retry System**: Automatic retry with exponential backoff
- 📸 **Error Screenshots**: Automatic screenshots for debugging failed downloads
- 🚨 **Error Detection**: Detect unavailable mods and deleted files
- 🔍 **Post-Download Verification**: Verify files actually downloaded successfully
- 🌐 **Rate Limit Detection**: Auto-adjust delays when Nexus Mods throttles requests

#### Advanced Features
- 👑 **Nexus Premium Support**: Direct API downloads for Premium members
- 🌐 **Selenium Integration**: More reliable browser automation with headless mode
- 🎯 **Multi-Browser Support**: Automatic detection and support for Chrome, Firefox, Edge
- 📦 **Multi-Collection Support**: Process multiple collections with duplicate detection
- ⚙️ **Persistent Configuration**: YAML config file to save preferences and click positions per game

#### Analytics & Reporting
- 📊 **Advanced Statistics**: Download speed, ETA, success rate dashboard
- 📈 **Progress Visualization**: Real-time graphs and detailed reports
- 📋 **Export Reports**: JSON/CSV export of download statistics
- 📝 **Detailed Logging**: Rotating logs with configurable verbosity

#### Data Management
- ✅ **Enhanced Progress Tracking**: JSON-based progress with timestamps and metadata
- 🔍 **Collection Validation**: Pre-flight checks for invalid mods
- 🧹 **Smart Tab Management**: Track actual open tabs instead of fixed batch size

### Development Priorities

**Phase 1 - Quick Wins** (1-2 weeks)
- Dry-run mode
- Smart retry system
- Enhanced logging
- YAML configuration
- Tab management improvements

**Phase 2 - User Experience** (1 month)
- Basic GUI (Tkinter)
- ✅ ~~Automatic button detection~~ **COMPLETED**
- Desktop notifications
- Pause/resume functionality

**Phase 3 - Advanced Features** (2-3 months)
- Selenium integration
- Nexus Premium API support
- Analytics dashboard
- Headless mode

See `IMPROVEMENTS.md` for detailed implementation roadmap.

---

**Made with ❤️ for the modding community**

*This tool respects Nexus Mods infrastructure and uses official collection formats.*

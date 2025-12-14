"""
Main command handler for CLI interface.
"""

from pathlib import Path

from src.domain.downloader_config import DownloaderConfig
from src.services.download_orchestrator import DownloadOrchestrator
from src.presentation.cli.argument_parser import parse_arguments
from src.presentation.console.formatter import ConsoleFormatter
from src.config.settings import Settings


def main():
    """Main entry point for the application."""
    args = parse_arguments()
    
    collection_file = Path(args.collection)
    
    if not collection_file.exists():
        print(f"Error: {collection_file} not found")
        return
    
    if args.reset_progress:
        progress_file = Path(args.progress_file)
        if progress_file.exists():
            progress_file.unlink()
            print(f"Progress file deleted: {progress_file}")
        else:
            print(f"No progress file to delete")
        return
    
    _print_instructions(args)
    
    if not args.yes:
        input("Press ENTER to continue...")
    
    config = DownloaderConfig(
        game_domain=args.game,
        delay_before_click=args.delay_click,
        delay_for_download=args.delay_download,
        delay_between_mods=args.delay_between,
        auto_close=not args.no_auto_close,
        progress_file=args.progress_file,
        force_focus=args.force_focus,
        batch_size=args.batch_size,
        use_auto_detection=args.auto_detect,
        template_path=args.template_path,
        detection_confidence=args.detection_confidence
    )
    
    downloader = None
    try:
        downloader = DownloadOrchestrator(collection_file, config)
        downloader.execute()
    except KeyboardInterrupt:
        print("\n\n[STOP] Stopped by user")
        if downloader:
            downloader.keyboard_listener.stop()
    except Exception as e:
        print(f"\nError: {e}")
        if downloader:
            downloader.keyboard_listener.stop()


def _print_instructions(args):
    """Print usage instructions."""
    formatter = ConsoleFormatter()
    
    formatter.print_header("NEXUS AUTO-DOWNLOADER")
    print()
    
    print("How it works:")
    formatter.print_requirement("1. First page opens")
    formatter.print_requirement("2. YOU click on 'SLOW DOWNLOAD' button")
    formatter.print_requirement("3. Your coordinates are recorded")
    formatter.print_requirement("4. Script automatically clicks at same position")
    formatter.print_requirement("   on all following pages")
    print()
    
    print("Configuration:")
    formatter.print_config_item("Collection", args.collection)
    formatter.print_config_item("Progress", args.progress_file)
    formatter.print_config_item("Click delay", f"{args.delay_click}s")
    
    if not args.no_auto_close:
        formatter.print_config_item("Auto-close", f"Yes (waits {args.delay_download}s before closing)")
        formatter.print_requirement("  -> Waits for download to start before closing tab")
    else:
        formatter.print_config_item("Auto-close", f"No (batch of {args.batch_size})")
        formatter.print_requirement(f"  -> Tabs stay open then closed every {args.batch_size} mods")
        formatter.print_requirement(f"  -> Faster but opens up to {args.batch_size} tabs")

    if args.auto_detect:
        formatter.print_config_item("Auto-detection", "Enabled")
        formatter.print_config_item("Template path", args.template_path)
        formatter.print_config_item("Confidence", f"{args.detection_confidence:.0%}")

    print()
    print("Make sure:")
    formatter.print_requirement("You are logged in to Nexus Mods")
    formatter.print_requirement("Your browser is in fullscreen")
    formatter.print_requirement("You don't move the window during process")
    print()
    print("Emergency stop:")
    formatter.print_requirement("Press F4 at any time to stop the script immediately")
    formatter.print_separator()
    print()

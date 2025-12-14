"""
Command-line argument parser.
"""

import argparse

from src.config.settings import Settings


def parse_arguments():
    """
    Parse command line arguments.
    
    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="Nexus Mods Auto-Downloader - Automate mod downloads from Nexus Mods",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python main.py
  python main.py --no-auto-close
  python main.py --collection my_mods.json
  python main.py --delay-click 3 --delay-download 8
  python main.py --reset-progress
        """
    )
    
    parser.add_argument(
        '--collection',
        default=Settings.DEFAULT_COLLECTION_FILE,
        help=f'Collection JSON file (default: {Settings.DEFAULT_COLLECTION_FILE})'
    )
    
    parser.add_argument(
        '--no-auto-close',
        action='store_true',
        help=f'Keep tabs open (batch close every {Settings.BATCH_SIZE} mods)'
    )
    
    parser.add_argument(
        '--progress-file',
        default=Settings.DEFAULT_PROGRESS_FILE,
        help=f'Progress tracking file (default: {Settings.DEFAULT_PROGRESS_FILE})'
    )
    
    parser.add_argument(
        '--reset-progress',
        action='store_true',
        help='Reset progress file'
    )
    
    parser.add_argument(
        '--delay-click',
        type=float,
        default=Settings.DEFAULT_DELAY_BEFORE_CLICK,
        help=f'Delay before clicking in seconds (default: {Settings.DEFAULT_DELAY_BEFORE_CLICK})'
    )
    
    parser.add_argument(
        '--delay-download',
        type=float,
        default=Settings.DEFAULT_DELAY_FOR_DOWNLOAD,
        help=f'Wait time for download start in seconds (default: {Settings.DEFAULT_DELAY_FOR_DOWNLOAD})'
    )
    
    parser.add_argument(
        '--delay-between',
        type=float,
        default=Settings.DEFAULT_DELAY_BETWEEN_MODS,
        help=f'Delay between mods in seconds (default: {Settings.DEFAULT_DELAY_BETWEEN_MODS})'
    )
    
    parser.add_argument(
        '--game',
        default=Settings.DEFAULT_GAME_DOMAIN,
        help=f'Game domain on Nexus Mods (default: {Settings.DEFAULT_GAME_DOMAIN})'
    )
    
    parser.add_argument(
        '--yes', '-y',
        action='store_true',
        help='Skip confirmation prompt'
    )

    parser.add_argument(
        '--force-focus',
        action='store_true',
        help='Force browser focus before each click (use if other windows appear on top)'
    )

    parser.add_argument(
        '--batch-size',
        type=int,
        default=Settings.BATCH_SIZE,
        help=f'Number of tabs to open before purge in batch mode (default: {Settings.BATCH_SIZE})'
    )

    return parser.parse_args()

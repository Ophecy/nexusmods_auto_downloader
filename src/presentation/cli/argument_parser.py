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
  python main.py -c my_mods.json -g cyberpunk2077
  python main.py -C 3 -D 8
  python main.py --reset-progress
  python main.py --fast
  python main.py --fast -C 3
        """
    )

    parser.add_argument(
        '--collection', '-c',
        default=Settings.DEFAULT_COLLECTION_FILE,
        help=f'Collection JSON file (default: {Settings.DEFAULT_COLLECTION_FILE})'
    )

    parser.add_argument(
        '--no-auto-close', '-n',
        action='store_true',
        default=None,
        help=f'Keep tabs open (batch close every {Settings.BATCH_SIZE} mods)'
    )

    parser.add_argument(
        '--progress-file', '-p',
        default=Settings.DEFAULT_PROGRESS_FILE,
        help=f'Progress tracking file (default: {Settings.DEFAULT_PROGRESS_FILE})'
    )

    parser.add_argument(
        '--reset-progress', '-r',
        action='store_true',
        help='Reset progress file'
    )

    parser.add_argument(
        '--delay-click', '-C',
        type=float,
        default=None,
        help=f'Delay before clicking in seconds (default: {Settings.DEFAULT_DELAY_BEFORE_CLICK})'
    )

    parser.add_argument(
        '--delay-download', '-D',
        type=float,
        default=None,
        help=f'Wait time for download start in seconds (default: {Settings.DEFAULT_DELAY_FOR_DOWNLOAD})'
    )

    parser.add_argument(
        '--delay-between', '-B',
        type=float,
        default=None,
        help=f'Delay between mods in seconds (default: {Settings.DEFAULT_DELAY_BETWEEN_MODS})'
    )

    parser.add_argument(
        '--game', '-g',
        default=Settings.DEFAULT_GAME_DOMAIN,
        help=f'Game domain on Nexus Mods (default: {Settings.DEFAULT_GAME_DOMAIN})'
    )

    parser.add_argument(
        '--yes', '-y',
        action='store_true',
        help='Skip confirmation prompt'
    )

    parser.add_argument(
        '--force-focus', '-f',
        action='store_true',
        help='Force browser focus before each click (use if other windows appear on top)'
    )

    parser.add_argument(
        '--batch-size', '-b',
        type=int,
        default=Settings.BATCH_SIZE,
        help=f'Number of tabs to open before purge in batch mode (default: {Settings.BATCH_SIZE})'
    )

    parser.add_argument(
        '--auto-detect', '-a',
        action='store_true',
        help='Use automatic button detection (OpenCV template matching)'
    )

    parser.add_argument(
        '--template-path', '-t',
        default=Settings.DEFAULT_TEMPLATE_PATH,
        help=f'Path to button template image (default: {Settings.DEFAULT_TEMPLATE_PATH})'
    )

    parser.add_argument(
        '--detection-confidence', '-d',
        type=float,
        default=Settings.DEFAULT_DETECTION_CONFIDENCE,
        help=f'Confidence threshold for detection 0-1 (default: {Settings.DEFAULT_DETECTION_CONFIDENCE})'
    )

    parser.add_argument(
        '--fast', '-F',
        action='store_true',
        help=(
            f'Fast preset: --no-auto-close, --delay-click {Settings.FAST_DELAY_CLICK}, '
            f'--delay-download {Settings.FAST_DELAY_DOWNLOAD}, --delay-between {Settings.FAST_DELAY_BETWEEN}. '
            'Explicit values override this preset.'
        )
    )

    return parser.parse_args()

"""
Presentation layer: User interfaces (CLI, console output).
"""

from src.presentation.cli.argument_parser import parse_arguments
from src.presentation.cli.command_handler import main

__all__ = ["parse_arguments", "main"]

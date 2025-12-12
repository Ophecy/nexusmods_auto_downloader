"""
Console output formatting utilities.
"""


class ConsoleFormatter:
    """Formats console output for better readability."""
    
    @staticmethod
    def print_separator(width: int = 60):
        """Print a separator line."""
        print("=" * width)
    
    @staticmethod
    def print_header(title: str, width: int = 60):
        """Print a formatted header."""
        print("\n" + "=" * width)
        print(title)
        print("=" * width)
    
    @staticmethod
    def print_section(title: str, items: list, width: int = 60):
        """Print a section with title and items."""
        print(f"\n{title}")
        for item in items:
            print(f"  {item}")
    
    @staticmethod
    def print_config_item(key: str, value: str):
        """Print a configuration item."""
        print(f"  • {key}: {value}")
    
    @staticmethod
    def print_requirement(text: str):
        """Print a requirement item."""
        print(f"  {text}")

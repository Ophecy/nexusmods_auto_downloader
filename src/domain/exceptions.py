"""
Custom exceptions for the domain layer.
"""


class NexusDownloaderException(Exception):
    """Base exception for all downloader errors."""
    pass


class NoClickRecordedException(NexusDownloaderException):
    """Raised when no click position was recorded."""
    pass


class CollectionNotFoundException(NexusDownloaderException):
    """Raised when collection file is not found."""
    pass


class InvalidCollectionFormatException(NexusDownloaderException):
    """Raised when collection file format is invalid."""
    pass

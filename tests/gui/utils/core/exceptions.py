"""Exceptions raised by GUI page-object utilities."""


class PageObjectNotFoundError(RuntimeError):
    """Raised when an item cannot be found in a page-object sequence."""

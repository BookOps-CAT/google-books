# -*- coding: utf-8 -*-


class GoogleBooksToolError(Exception):
    """Base class for exceptions in this module"""

    pass


class FileNameError(GoogleBooksToolError):
    """
    Exception raised when file name violates projects naming conventions.
    """

    pass

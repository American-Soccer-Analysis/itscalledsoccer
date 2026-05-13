"""Custom exception classes for the American Soccer Analysis client."""


class ASAError(Exception):
    """Base exception for all American Soccer Analysis client errors."""

    pass


class InvalidEntityTypeError(ASAError):
    """Raised when an unknown entity type is provided."""

    pass


class InvalidLeagueError(ASAError):
    """Raised when an invalid league is provided."""

    pass


class SalaryDataError(ASAError):
    """Raised when salary data is requested from an unsupported league."""

    pass


class ConflictingParametersError(ASAError):
    """Raised when conflicting parameters are provided."""

    pass


class InvalidParameterFormatError(ASAError):
    """Raised when a parameter has an invalid format or type."""

    pass


class InvalidSeasonError(ASAError):
    """Raised when a season is before 2013"""

    pass

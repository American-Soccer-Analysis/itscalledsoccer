"""Custom exception classes for the American Soccer Analysis client."""


class ASAError(Exception):
    """Base exception for all American Soccer Analysis client errors."""


class InvalidEntityTypeError(ASAError):
    """Raised when an unknown entity type is provided."""


class InvalidLeagueError(ASAError):
    """Raised when an invalid league is provided."""


class SalaryDataError(ASAError):
    """Raised when salary data is requested from an unsupported league."""


class ConflictingParametersError(ASAError):
    """Raised when conflicting parameters are provided."""


class InvalidParameterFormatError(ASAError):
    """Raised when a parameter has an invalid format or type."""


class InvalidSeasonError(ASAError):
    """Raised when a season is before 2013"""

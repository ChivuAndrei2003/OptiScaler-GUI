class OptiScalerError(Exception):
    """Base exception for expected application failures."""


class InvalidPackageError(OptiScalerError):
    """Raised when an OptiScaler package cannot be used."""


class GameNotFoundError(OptiScalerError):
    """Raised when a configured game path is missing or invalid."""


class InjectionBackendError(OptiScalerError):
    """Raised when the selected platform backend cannot complete an operation."""

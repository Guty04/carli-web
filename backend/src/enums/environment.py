"""Environment enumeration for ."""

from enum import StrEnum, auto


class Environment(StrEnum):
    """Application environment types."""

    DEVELOPMENT = auto()
    STAGING = auto()
    PRODUCTION = auto()

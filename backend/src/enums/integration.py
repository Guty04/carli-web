from enum import StrEnum, auto


class Integration(StrEnum):
    GITLAB = auto()
    JIRA = auto()
    SONARQUBE = auto()
    LOGFIRE = auto()
    INFISICAL = auto()

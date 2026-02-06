from enum import StrEnum, auto


class Permission(StrEnum):
    CREATE_PROJECT = auto()
    READ_PROJECT = auto()
    READ_PROJECTS = auto()

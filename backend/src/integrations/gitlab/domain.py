from enum import IntEnum


class AccessLevel(IntEnum):
    NO_ACCESS = 0
    REPORTER = 20
    DEVELOPER = 30
    MAINTAINER = 40
    OWNER = 50

import re
import unicodedata


def slugify(name: str) -> str:
    """Convert a project name to an uppercase alphanumeric key."""

    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    name = re.sub(r"[^a-zA-Z0-9]", "", name).upper()
    name = name.lstrip("0123456789")
    return name[:10]


def logfire_slug(name: str) -> str:
    """Convert a project name to a Logfire-compatible slug (lowercase, hyphen-separated)."""

    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    name = re.sub(r"[^a-zA-Z0-9]+", "-", name).strip("-").lower()
    return re.sub(r"-+", "-", name)

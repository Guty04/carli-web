import re
import unicodedata


def slugify(name: str) -> str:
    """Convert a project name to a slug matching ``^[a-z0-9]+(?:-[a-z0-9]+)*$``."""
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    name = name.lower()
    name = re.sub(r"[^a-z0-9]+", "-", name)
    return name.strip("-")

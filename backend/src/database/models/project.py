from uuid import UUID

from sqlalchemy import UUID as SQLUUID
from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Project(Base):
    __tablename__: str = "project"
    __table_args__ = {"comment": "Projects created and managed by the platform"}

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    name: Mapped[str] = mapped_column(String(150), comment="Project display name")
    id_user: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("user.id"),
        comment="User who created the project",
    )
    id_project_gitlab: Mapped[int] = mapped_column(unique=True, comment="GitLab project ID")
    description: Mapped[str | None] = mapped_column(
        String(500), nullable=True, comment="Project description for README"
    )
    url_repository: Mapped[str] = mapped_column(String(500), comment="SSH clone URL from GitLab")
    id_project_logfire: Mapped[str | None] = mapped_column(String(36), nullable=True, comment="Logfire project UUID")
    web_domain: Mapped[str | None] = mapped_column(String(), nullable=True, comment="Web domain for the server.")

from uuid import UUID

from sqlalchemy import UUID as SQLUUID
from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .integration import Integration


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
    description: Mapped[str] = mapped_column(String(500), comment="Project description for README")
    url_repository: Mapped[str] = mapped_column(String(500), comment="SSH clone URL from GitLab")
    web_domain: Mapped[str | None] = mapped_column(String(), nullable=True, comment="Web domain for the server.")

    integrations: Mapped[set[Integration]] = relationship(
        cascade="all, delete-orphan",
    )

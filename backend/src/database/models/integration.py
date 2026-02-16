from uuid import UUID

from sqlalchemy import Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.enums import Integration as IntegrationEnum

from .base import Base


class Integration(Base):
    __tablename__ = "integration"
    __table_args__ = {"comment": "External integration references for projects"}

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=func.gen_random_uuid(),
        comment="Integration record ID",
    )
    project_id: Mapped[UUID] = mapped_column(
        ForeignKey("project.id", ondelete="CASCADE"),
        nullable=False,
        comment="FK to project",
    )
    name: Mapped[IntegrationEnum] = mapped_column(
        Enum(IntegrationEnum, name="integration_type"),
        nullable=False,
        comment="Integration name (e.g., GITLAB, INFISICAL)",
    )
    external_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="External ID in the integration system",
    )

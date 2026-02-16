"""Population database

Revision ID: 96d4982bbaa5
Revises: 126316e40014
Create Date: 2026-02-15 23:22:27.293799

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "96d4982bbaa5"
down_revision: Union[str, Sequence[str], None] = "126316e40014"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        INSERT INTO role (name, is_active)
        VALUES
            ('administrator', TRUE),
            ('manager', TRUE)
        """)
    op.execute("""
        INSERT INTO permission (name, is_active)
        VALUES
            ('create_project', TRUE),
            ('read_project', TRUE),
            ('read_projects', TRUE),
            ('read_users', TRUE)
        """)
    op.execute("""
        INSERT INTO role_x_permission (id_role, id_permission, is_active)
        SELECT r.id, p.id, TRUE
        FROM role r, permission p
        WHERE r.name = 'administrator'
        """)
    op.execute("""
        INSERT INTO role_x_permission (id_role, id_permission, is_active)
        SELECT r.id, p.id, TRUE
        FROM role r
        JOIN permission p ON p.name IN ('read_project')
        WHERE r.name = 'manager'
        """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        DELETE FROM role_x_permission
        WHERE id_role IN (
            SELECT id FROM role WHERE name IN ('administrator', 'manager')
        )
    """)

    op.execute("""
        DELETE FROM permission
        WHERE name IN (
            'create_project',
            'read_project',
            'read_projects',
            'read_users'
        )
    """)

    op.execute("""
        DELETE FROM role
        WHERE name IN ('administrator', 'manager')
    """)

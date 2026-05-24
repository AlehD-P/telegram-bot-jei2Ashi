"""initial schema

Revision ID: 0001_initial
Revises: 
Create Date: 2026-05-24
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("telegram_user_id", sa.BigInteger(), nullable=False),
        sa.Column("username", sa.String(length=255), nullable=True),
    )
    op.create_index("ix_users_telegram_user_id", "users", ["telegram_user_id"], unique=True)

    op.create_table(
        "chats",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("telegram_chat_id", sa.BigInteger(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=True),
    )
    op.create_index("ix_chats_telegram_chat_id", "chats", ["telegram_chat_id"], unique=True)

    op.create_table(
        "sessions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("state", sa.String(length=255), nullable=False, server_default=sa.text("'active'")),
    )

    op.create_table(
        "update_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("update_type", sa.String(length=100), nullable=False),
    )

    op.create_table(
        "file_objects",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("storage_key", sa.String(length=255), nullable=False),
    )
    op.create_index("ix_file_objects_storage_key", "file_objects", ["storage_key"], unique=True)

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("event", sa.String(length=255), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("audit_logs")
    op.drop_index("ix_file_objects_storage_key", table_name="file_objects")
    op.drop_table("file_objects")
    op.drop_table("update_logs")
    op.drop_table("sessions")
    op.drop_index("ix_chats_telegram_chat_id", table_name="chats")
    op.drop_table("chats")
    op.drop_index("ix_users_telegram_user_id", table_name="users")
    op.drop_table("users")

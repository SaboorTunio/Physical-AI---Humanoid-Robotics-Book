"""
Initial database schema creation.
Creates all tables for Living Textbook RAG Backend.

Revision ID: 001
Revises: None
Create Date: 2025-01-15 10:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

# Revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create initial database schema."""

    # Create chapters table
    op.create_table(
        'chapters',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('index', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('module', sa.Integer(), nullable=False),
        sa.Column('part', sa.Integer(), nullable=False),
        sa.Column('learning_objectives', sa.JSON(), nullable=False),
        sa.Column('keywords', sa.JSON(), nullable=False),
        sa.Column('prerequisites', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('index'),
    )
    op.create_index('idx_chapter_module_part', 'chapters', ['module', 'part'])
    op.create_index('ix_chapters_index', 'chapters', ['index'])

    # Create chunk_vectors table
    op.create_table(
        'chunk_vectors',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('chapter_id', sa.String(36), nullable=False),
        sa.Column('chunk_index', sa.Integer(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('embedding', sa.JSON(), nullable=False),
        sa.Column('token_count', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['chapter_id'], ['chapters.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('idx_chunk_chapter_index', 'chunk_vectors', ['chapter_id', 'chunk_index'])
    op.create_index('ix_chunk_vectors_chapter_id', 'chunk_vectors', ['chapter_id'])

    # Create chat_sessions table
    op.create_table(
        'chat_sessions',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('user_id', sa.String(255), nullable=True),
        sa.Column('chapter_context', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('message_count', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('last_activity_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('idx_session_user_active', 'chat_sessions', ['user_id', 'is_active'])
    op.create_index('ix_chat_sessions_created_at', 'chat_sessions', ['created_at'])
    op.create_index('ix_chat_sessions_updated_at', 'chat_sessions', ['updated_at'])
    op.create_index('ix_chat_sessions_user_id', 'chat_sessions', ['user_id'])

    # Create chat_messages table
    op.create_table(
        'chat_messages',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('session_id', sa.String(36), nullable=False),
        sa.Column('role', sa.String(10), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('highlighted_context', sa.Text(), nullable=True),
        sa.Column('source_chunks', sa.JSON(), nullable=True),
        sa.Column('confidence', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['session_id'], ['chat_sessions.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('idx_message_session_role', 'chat_messages', ['session_id', 'role'])
    op.create_index('ix_chat_messages_created_at', 'chat_messages', ['created_at'])
    op.create_index('ix_chat_messages_session_id', 'chat_messages', ['session_id'])

    # Create ingestion_logs table
    op.create_table(
        'ingestion_logs',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('chapter_id', sa.String(36), nullable=False),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('chunks_created', sa.Integer(), nullable=False),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('duration_seconds', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['chapter_id'], ['chapters.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('idx_ingestion_chapter_status', 'ingestion_logs', ['chapter_id', 'status'])
    op.create_index('ix_ingestion_logs_created_at', 'ingestion_logs', ['created_at'])


def downgrade() -> None:
    """Drop all tables."""
    op.drop_table('ingestion_logs')
    op.drop_table('chat_messages')
    op.drop_table('chat_sessions')
    op.drop_table('chunk_vectors')
    op.drop_table('chapters')

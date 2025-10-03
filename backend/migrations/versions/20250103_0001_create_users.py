"""Create users table

Revision ID: 0001
Revises:
Create Date: 2025-01-03

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM

# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create users table with authentication support."""
    # Create auth_provider enum
    auth_provider_enum = ENUM(
        'LOCAL',
        'AZURE_AD',
        name='auth_provider_enum',
        create_type=True
    )
    auth_provider_enum.create(op.get_bind())

    # Create users table
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('username', sa.String(100), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=True),
        sa.Column('full_name', sa.String(200), nullable=True),
        sa.Column('auth_provider', auth_provider_enum, nullable=False, server_default='LOCAL'),
        sa.Column('external_id', sa.String(255), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('last_login_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email', name='uq_user_email'),
        sa.UniqueConstraint('username', name='uq_user_username')
    )

    # Create indexes
    op.create_index('ix_user_email', 'user', ['email'])
    op.create_index('ix_user_username', 'user', ['username'])
    op.create_index('ix_user_external_id', 'user', ['external_id', 'auth_provider'])


def downgrade() -> None:
    """Drop users table."""
    op.drop_index('ix_user_external_id', table_name='user')
    op.drop_index('ix_user_username', table_name='user')
    op.drop_index('ix_user_email', table_name='user')
    op.drop_table('user')

    # Drop enum type
    auth_provider_enum = ENUM(
        'LOCAL',
        'AZURE_AD',
        name='auth_provider_enum'
    )
    auth_provider_enum.drop(op.get_bind())

"""Create diagram repository tables

Revision ID: 0003
Revises: 0002
Create Date: 2025-01-03

Creates Diagram, DiagramObject, and DiagramRelationship tables.
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, ENUM

# revision identifiers, used by Alembic.
revision = '0003'
down_revision = '0002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create diagram repository tables."""

    # Create object_type enum for diagram objects
    object_type_enum = ENUM(
        'SUPERDOMAIN',
        'DOMAIN',
        'ENTITY',
        name='object_type_enum',
        create_type=True
    )
    object_type_enum.create(op.get_bind())

    # 1. Diagram table
    op.create_table(
        'diagram',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('purpose', sa.Text(), nullable=True),
        sa.Column('tags', JSONB, nullable=True),
        sa.Column('canvas_settings', JSONB, nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('last_modified_by', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['created_by'], ['user.id'], name='fk_diagram_created_by'),
        sa.ForeignKeyConstraint(['last_modified_by'], ['user.id'], name='fk_diagram_last_modified_by')
    )

    # 2. DiagramObject table
    op.create_table(
        'diagram_object',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('diagram_id', sa.Integer(), nullable=False),
        sa.Column('object_type', object_type_enum, nullable=False),
        sa.Column('object_id', sa.Integer(), nullable=False),
        sa.Column('position_x', sa.Float(), nullable=False),
        sa.Column('position_y', sa.Float(), nullable=False),
        sa.Column('width', sa.Float(), nullable=True),
        sa.Column('height', sa.Float(), nullable=True),
        sa.Column('z_index', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('visual_style', JSONB, nullable=True),
        sa.Column('is_collapsed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['diagram_id'], ['diagram.id'], name='fk_diagram_object_diagram', ondelete='CASCADE'),
        sa.UniqueConstraint('diagram_id', 'object_type', 'object_id', name='uq_diagram_object_unique')
    )

    # 3. DiagramRelationship table
    op.create_table(
        'diagram_relationship',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('diagram_id', sa.Integer(), nullable=False),
        sa.Column('relationship_id', sa.Integer(), nullable=False),
        sa.Column('is_visible', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('path_points', JSONB, nullable=True),
        sa.Column('source_anchor', sa.String(20), nullable=True),
        sa.Column('target_anchor', sa.String(20), nullable=True),
        sa.Column('visual_style', JSONB, nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['diagram_id'], ['diagram.id'], name='fk_diagram_relationship_diagram', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['relationship_id'], ['relationship.id'], name='fk_diagram_relationship_relationship', ondelete='CASCADE'),
        sa.UniqueConstraint('diagram_id', 'relationship_id', name='uq_diagram_relationship_unique')
    )


def downgrade() -> None:
    """Drop diagram repository tables."""
    op.drop_table('diagram_relationship')
    op.drop_table('diagram_object')
    op.drop_table('diagram')

    # Drop enum type
    object_type_enum = ENUM(
        'SUPERDOMAIN',
        'DOMAIN',
        'ENTITY',
        name='object_type_enum'
    )
    object_type_enum.drop(op.get_bind())

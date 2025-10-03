"""Create object repository tables

Revision ID: 0002
Revises: 0001
Create Date: 2025-01-03

Creates Superdomain, Domain, Entity, Attribute, and Relationship tables.
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, ENUM

# revision identifiers, used by Alembic.
revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create object repository tables."""

    # Create cardinality enum for relationships
    cardinality_enum = ENUM(
        'ZERO_ONE',
        'ONE',
        'ZERO_MANY',
        'ONE_MANY',
        name='cardinality_enum',
        create_type=True
    )
    cardinality_enum.create(op.get_bind())

    # 1. Superdomain table
    op.create_table(
        'superdomain',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name', name='uq_superdomain_name'),
        sa.ForeignKeyConstraint(['created_by'], ['user.id'], name='fk_superdomain_created_by')
    )

    # 2. Domain table
    op.create_table(
        'domain',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('superdomain_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['superdomain_id'], ['superdomain.id'], name='fk_domain_superdomain', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['created_by'], ['user.id'], name='fk_domain_created_by'),
        sa.UniqueConstraint('superdomain_id', 'name', name='uq_domain_superdomain_name')
    )

    # 3. Entity table
    op.create_table(
        'entity',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('domain_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['domain_id'], ['domain.id'], name='fk_entity_domain', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['created_by'], ['user.id'], name='fk_entity_created_by'),
        sa.UniqueConstraint('domain_id', 'name', name='uq_entity_domain_name')
    )

    # 4. Attribute table (BIGINT for 100K+ attributes)
    op.create_table(
        'attribute',
        sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('entity_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('data_type', sa.String(50), nullable=False),
        sa.Column('is_nullable', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('default_value', sa.String(255), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('constraints', JSONB, nullable=True),
        sa.Column('data_quality_rules', JSONB, nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['entity_id'], ['entity.id'], name='fk_attribute_entity', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['created_by'], ['user.id'], name='fk_attribute_created_by'),
        sa.UniqueConstraint('entity_id', 'name', name='uq_attribute_entity_name')
    )

    # 5. Relationship table
    op.create_table(
        'relationship',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('source_entity_id', sa.Integer(), nullable=False),
        sa.Column('target_entity_id', sa.Integer(), nullable=False),
        sa.Column('source_attribute_id', sa.BigInteger(), nullable=True),
        sa.Column('target_attribute_id', sa.BigInteger(), nullable=True),
        sa.Column('name', sa.String(100), nullable=True),
        sa.Column('source_role', sa.String(100), nullable=True),
        sa.Column('target_role', sa.String(100), nullable=True),
        sa.Column('source_cardinality', cardinality_enum, nullable=False),
        sa.Column('target_cardinality', cardinality_enum, nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['source_entity_id'], ['entity.id'], name='fk_relationship_source_entity', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['target_entity_id'], ['entity.id'], name='fk_relationship_target_entity', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['source_attribute_id'], ['attribute.id'], name='fk_relationship_source_attribute'),
        sa.ForeignKeyConstraint(['target_attribute_id'], ['attribute.id'], name='fk_relationship_target_attribute'),
        sa.ForeignKeyConstraint(['created_by'], ['user.id'], name='fk_relationship_created_by')
    )


def downgrade() -> None:
    """Drop object repository tables."""
    op.drop_table('relationship')
    op.drop_table('attribute')
    op.drop_table('entity')
    op.drop_table('domain')
    op.drop_table('superdomain')

    # Drop enum type
    cardinality_enum = ENUM(
        'ZERO_ONE',
        'ONE',
        'ZERO_MANY',
        'ONE_MANY',
        name='cardinality_enum'
    )
    cardinality_enum.drop(op.get_bind())

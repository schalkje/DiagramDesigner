"""Create performance indexes

Revision ID: 0004
Revises: 0003
Create Date: 2025-01-03

Creates indexes for common query patterns based on data-model.md performance section.
"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '0004'
down_revision = '0003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create indexes for common queries."""

    # Object Repository indexes

    # Query domains by superdomain
    op.create_index('ix_domain_superdomain_id', 'domain', ['superdomain_id'])

    # Query entities by domain
    op.create_index('ix_entity_domain_id', 'entity', ['domain_id'])

    # Query attributes by entity
    op.create_index('ix_attribute_entity_id', 'attribute', ['entity_id'])

    # Query relationships by entity (both source and target)
    op.create_index('ix_relationship_source_entity_id', 'relationship', ['source_entity_id'])
    op.create_index('ix_relationship_target_entity_id', 'relationship', ['target_entity_id'])
    # Composite index for finding relationships between two entities
    op.create_index('ix_relationship_source_target', 'relationship', ['source_entity_id', 'target_entity_id'])

    # Diagram Repository indexes

    # Query diagram objects by diagram
    op.create_index('ix_diagram_object_diagram_id', 'diagram_object', ['diagram_id'])

    # Reverse lookup: which diagrams contain an object
    op.create_index('ix_diagram_object_lookup', 'diagram_object', ['object_type', 'object_id'])

    # Query diagram relationships by diagram
    op.create_index('ix_diagram_relationship_diagram_id', 'diagram_relationship', ['diagram_id'])

    # Query diagram relationships by relationship (for cascade updates)
    op.create_index('ix_diagram_relationship_relationship_id', 'diagram_relationship', ['relationship_id'])

    # Query diagrams by user
    op.create_index('ix_diagram_created_by', 'diagram', ['created_by'])

    # Tag-based diagram search (GIN index for JSONB)
    op.create_index('ix_diagram_tags', 'diagram', ['tags'], postgresql_using='gin')

    # Timestamps for sorting (most recent first)
    op.create_index('ix_diagram_updated_at', 'diagram', ['updated_at'], postgresql_ops={'updated_at': 'DESC'})
    op.create_index('ix_entity_updated_at', 'entity', ['updated_at'], postgresql_ops={'updated_at': 'DESC'})
    op.create_index('ix_superdomain_updated_at', 'superdomain', ['updated_at'], postgresql_ops={'updated_at': 'DESC'})


def downgrade() -> None:
    """Drop performance indexes."""

    # Object Repository indexes
    op.drop_index('ix_domain_superdomain_id', table_name='domain')
    op.drop_index('ix_entity_domain_id', table_name='entity')
    op.drop_index('ix_attribute_entity_id', table_name='attribute')
    op.drop_index('ix_relationship_source_entity_id', table_name='relationship')
    op.drop_index('ix_relationship_target_entity_id', table_name='relationship')
    op.drop_index('ix_relationship_source_target', table_name='relationship')

    # Diagram Repository indexes
    op.drop_index('ix_diagram_object_diagram_id', table_name='diagram_object')
    op.drop_index('ix_diagram_object_lookup', table_name='diagram_object')
    op.drop_index('ix_diagram_relationship_diagram_id', table_name='diagram_relationship')
    op.drop_index('ix_diagram_relationship_relationship_id', table_name='diagram_relationship')
    op.drop_index('ix_diagram_created_by', table_name='diagram')
    op.drop_index('ix_diagram_tags', table_name='diagram')

    # Timestamp indexes
    op.drop_index('ix_diagram_updated_at', table_name='diagram')
    op.drop_index('ix_entity_updated_at', table_name='entity')
    op.drop_index('ix_superdomain_updated_at', table_name='superdomain')

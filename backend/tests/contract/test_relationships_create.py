"""Contract test for POST /relationships endpoint.

Validates RelationshipCreate schema with cardinality enums.
Expected to FAIL until implementation (TDD).
"""
import pytest


def test_create_relationship_success(api_client, auth_headers):
    """Test POST /relationships creates relationship and returns 201."""
    # Assumes two entities exist with IDs 1 and 2
    response = api_client.post('/api/v1/relationships', headers=auth_headers, json={
        'sourceEntityId': 1,
        'targetEntityId': 2,
        'sourceRole': 'customer',
        'targetRole': 'orders',
        'sourceCardinality': 'ONE',
        'targetCardinality': 'ZERO_MANY',
        'description': 'Customer has many orders'
    })

    # Should return 201 Created
    assert response.status_code == 201
    assert response.content_type == 'application/json'

    # Validate response matches Relationship schema
    data = response.json
    assert 'id' in data
    assert 'sourceEntityId' in data
    assert 'targetEntityId' in data
    assert 'sourceRole' in data
    assert 'targetRole' in data
    assert 'sourceCardinality' in data
    assert 'targetCardinality' in data
    assert 'createdAt' in data
    assert 'updatedAt' in data

    # Validate values
    assert data['sourceEntityId'] == 1
    assert data['targetEntityId'] == 2
    assert data['sourceCardinality'] == 'ONE'
    assert data['targetCardinality'] == 'ZERO_MANY'


def test_create_relationship_missing_source_entity_returns_400(api_client, auth_headers):
    """Test POST /relationships without required sourceEntityId returns 400."""
    response = api_client.post('/api/v1/relationships', headers=auth_headers, json={
        'targetEntityId': 2,
        'sourceCardinality': 'ONE',
        'targetCardinality': 'ZERO_MANY'
    })

    # Should return 400 Bad Request
    assert response.status_code == 400


def test_create_relationship_invalid_cardinality_returns_400(api_client, auth_headers):
    """Test POST /relationships with invalid cardinality enum returns 400."""
    response = api_client.post('/api/v1/relationships', headers=auth_headers, json={
        'sourceEntityId': 1,
        'targetEntityId': 2,
        'sourceCardinality': 'INVALID',
        'targetCardinality': 'ZERO_MANY'
    })

    # Should return 400 Bad Request (cardinality not in enum)
    assert response.status_code == 400


def test_create_relationship_all_valid_cardinalities(api_client, auth_headers):
    """Test POST /relationships with all valid cardinality values."""
    valid_cardinalities = ['ZERO_ONE', 'ONE', 'ZERO_MANY', 'ONE_MANY']

    for source_card in valid_cardinalities:
        for target_card in valid_cardinalities:
            response = api_client.post('/api/v1/relationships', headers=auth_headers, json={
                'sourceEntityId': 1,
                'targetEntityId': 2,
                'sourceCardinality': source_card,
                'targetCardinality': target_card
            })

            # Should return 201 Created for all valid combinations
            assert response.status_code == 201
            data = response.json
            assert data['sourceCardinality'] == source_card
            assert data['targetCardinality'] == target_card


def test_create_relationship_self_referential(api_client, auth_headers):
    """Test POST /relationships with source == target (self-referential)."""
    response = api_client.post('/api/v1/relationships', headers=auth_headers, json={
        'sourceEntityId': 1,
        'targetEntityId': 1,  # Self-referential
        'sourceRole': 'parent',
        'targetRole': 'children',
        'sourceCardinality': 'ZERO_ONE',
        'targetCardinality': 'ZERO_MANY'
    })

    # Should return 201 Created (self-referential allowed)
    assert response.status_code == 201


def test_create_relationship_invalid_entity_returns_400(api_client, auth_headers):
    """Test POST /relationships with non-existent entity returns 400."""
    response = api_client.post('/api/v1/relationships', headers=auth_headers, json={
        'sourceEntityId': 99999,
        'targetEntityId': 2,
        'sourceCardinality': 'ONE',
        'targetCardinality': 'ZERO_MANY'
    })

    # Should return 400 Bad Request (foreign key constraint)
    assert response.status_code == 400


def test_create_relationship_multiple_between_same_entities(api_client, auth_headers):
    """Test POST /relationships allows multiple relationships between same entities with different roles."""
    # First relationship
    response1 = api_client.post('/api/v1/relationships', headers=auth_headers, json={
        'sourceEntityId': 1,
        'targetEntityId': 2,
        'sourceRole': 'primary_customer',
        'targetRole': 'primary_orders',
        'sourceCardinality': 'ONE',
        'targetCardinality': 'ZERO_MANY'
    })
    assert response1.status_code == 201

    # Second relationship (same entities, different roles)
    response2 = api_client.post('/api/v1/relationships', headers=auth_headers, json={
        'sourceEntityId': 1,
        'targetEntityId': 2,
        'sourceRole': 'billing_customer',
        'targetRole': 'billing_orders',
        'sourceCardinality': 'ZERO_ONE',
        'targetCardinality': 'ZERO_MANY'
    })
    # Should allow multiple relationships with unique roles
    assert response2.status_code == 201


def test_create_relationship_requires_auth(api_client):
    """Test POST /relationships without auth returns 401."""
    response = api_client.post('/api/v1/relationships', json={
        'sourceEntityId': 1,
        'targetEntityId': 2,
        'sourceCardinality': 'ONE',
        'targetCardinality': 'ZERO_MANY'
    })

    # Should return 401 Unauthorized
    assert response.status_code == 401

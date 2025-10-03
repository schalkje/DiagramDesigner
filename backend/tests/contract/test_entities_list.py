"""Contract test for GET /entities endpoint.

Validates filtering by domainId and Entity schema.
Expected to FAIL until implementation (TDD).
"""
import pytest


def test_list_entities_returns_paginated_data(api_client, auth_headers):
    """Test GET /entities returns paginated list."""
    response = api_client.get('/api/v1/entities', headers=auth_headers)

    # Should return 200 OK
    assert response.status_code == 200
    assert response.content_type == 'application/json'

    # Validate response structure
    data = response.json
    assert 'data' in data
    assert 'pagination' in data
    assert isinstance(data['data'], list)


def test_list_entities_filter_by_domain_id(api_client, auth_headers, sample_domain_id):
    """Test GET /entities with domainId filter."""
    response = api_client.get(
        f'/api/v1/entities?domainId={sample_domain_id}',
        headers=auth_headers
    )

    # Should return 200 OK
    assert response.status_code == 200
    data = response.json

    # All returned entities should belong to specified domain
    for entity in data['data']:
        assert 'domainId' in entity
        assert entity['domainId'] == sample_domain_id


def test_list_entities_validates_entity_schema(api_client, auth_headers):
    """Test entity objects match OpenAPI Entity schema."""
    response = api_client.get('/api/v1/entities', headers=auth_headers)

    assert response.status_code == 200
    data = response.json

    if len(data['data']) > 0:
        entity = data['data'][0]
        assert 'id' in entity
        assert 'domainId' in entity
        assert 'name' in entity
        assert 'createdAt' in entity
        assert 'updatedAt' in entity

        # Validate types
        assert isinstance(entity['id'], int)
        assert isinstance(entity['domainId'], int)
        assert isinstance(entity['name'], str)


def test_list_entities_requires_auth(api_client):
    """Test GET /entities without auth returns 401."""
    response = api_client.get('/api/v1/entities')

    assert response.status_code == 401

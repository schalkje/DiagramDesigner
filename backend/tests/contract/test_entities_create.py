"""Contract test for POST /entities endpoint.

Validates EntityCreate schema with domainId.
Expected to FAIL until implementation (TDD).
"""
import pytest


def test_create_entity_success(api_client, auth_headers, sample_domain_id):
    """Test POST /entities creates entity and returns 201."""
    response = api_client.post('/api/v1/entities', headers=auth_headers, json={
        'domainId': sample_domain_id,
        'name': 'Customer',
        'description': 'Customer information'
    })

    # Should return 201 Created
    assert response.status_code == 201
    assert response.content_type == 'application/json'

    # Validate response matches Entity schema
    data = response.json
    assert 'id' in data
    assert 'domainId' in data
    assert 'name' in data
    assert 'description' in data
    assert 'createdAt' in data
    assert 'updatedAt' in data

    # Validate values
    assert data['domainId'] == sample_domain_id
    assert data['name'] == 'Customer'
    assert data['description'] == 'Customer information'


def test_create_entity_missing_domain_id_returns_400(api_client, auth_headers):
    """Test POST /entities without required domainId returns 400."""
    response = api_client.post('/api/v1/entities', headers=auth_headers, json={
        'name': 'Customer',
        'description': 'Missing domain'
    })

    # Should return 400 Bad Request
    assert response.status_code == 400


def test_create_entity_missing_name_returns_400(api_client, auth_headers, sample_domain_id):
    """Test POST /entities without required name returns 400."""
    response = api_client.post('/api/v1/entities', headers=auth_headers, json={
        'domainId': sample_domain_id,
        'description': 'Missing name'
    })

    # Should return 400 Bad Request
    assert response.status_code == 400


def test_create_entity_invalid_domain_id_returns_400(api_client, auth_headers):
    """Test POST /entities with non-existent domainId returns 400."""
    response = api_client.post('/api/v1/entities', headers=auth_headers, json={
        'domainId': 99999,
        'name': 'Customer',
        'description': 'Invalid parent'
    })

    # Should return 400 Bad Request (foreign key constraint)
    assert response.status_code == 400


def test_create_entity_name_too_long_returns_400(api_client, auth_headers, sample_domain_id):
    """Test POST /entities with name >100 chars returns 400."""
    response = api_client.post('/api/v1/entities', headers=auth_headers, json={
        'domainId': sample_domain_id,
        'name': 'x' * 101,
        'description': 'Test'
    })

    # Should return 400 Bad Request (maxLength: 100)
    assert response.status_code == 400


def test_create_entity_duplicate_name_in_domain_returns_400(api_client, auth_headers, sample_domain_id):
    """Test POST /entities with duplicate name in same domain returns 400."""
    # Create first entity
    api_client.post('/api/v1/entities', headers=auth_headers, json={
        'domainId': sample_domain_id,
        'name': 'UniqueEntity',
        'description': 'First'
    })

    # Try to create duplicate in same domain
    response = api_client.post('/api/v1/entities', headers=auth_headers, json={
        'domainId': sample_domain_id,
        'name': 'UniqueEntity',
        'description': 'Duplicate'
    })

    # Should return 400 Bad Request (unique constraint: domain_id, name)
    assert response.status_code == 400


def test_create_entity_requires_auth(api_client, sample_domain_id):
    """Test POST /entities without auth returns 401."""
    response = api_client.post('/api/v1/entities', json={
        'domainId': sample_domain_id,
        'name': 'Customer'
    })

    # Should return 401 Unauthorized
    assert response.status_code == 401

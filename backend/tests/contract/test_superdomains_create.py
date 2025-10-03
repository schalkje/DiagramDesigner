"""Contract test for POST /superdomains endpoint.

Validates SuperdomainCreate schema and 201 response.
Expected to FAIL until implementation (TDD).
"""
import pytest


def test_create_superdomain_success(api_client, auth_headers):
    """Test POST /superdomains creates superdomain and returns 201."""
    response = api_client.post('/api/v1/superdomains', headers=auth_headers, json={
        'name': 'Business',
        'description': 'Business-related data models'
    })

    # Should return 201 Created
    assert response.status_code == 201
    assert response.content_type == 'application/json'

    # Validate response matches Superdomain schema
    data = response.json
    assert 'id' in data
    assert 'name' in data
    assert 'description' in data
    assert 'createdAt' in data
    assert 'updatedAt' in data

    # Validate values
    assert data['name'] == 'Business'
    assert data['description'] == 'Business-related data models'
    assert isinstance(data['id'], int)


def test_create_superdomain_missing_name_returns_400(api_client, auth_headers):
    """Test POST /superdomains without required name returns 400."""
    response = api_client.post('/api/v1/superdomains', headers=auth_headers, json={
        'description': 'Missing name'
    })

    # Should return 400 Bad Request
    assert response.status_code == 400


def test_create_superdomain_name_too_long_returns_400(api_client, auth_headers):
    """Test POST /superdomains with name >100 chars returns 400."""
    response = api_client.post('/api/v1/superdomains', headers=auth_headers, json={
        'name': 'x' * 101,
        'description': 'Test'
    })

    # Should return 400 Bad Request (maxLength: 100 in OpenAPI spec)
    assert response.status_code == 400


def test_create_superdomain_duplicate_name_returns_400(api_client, auth_headers):
    """Test POST /superdomains with duplicate name returns 400."""
    # Create first superdomain
    api_client.post('/api/v1/superdomains', headers=auth_headers, json={
        'name': 'UniqueTest',
        'description': 'First'
    })

    # Try to create duplicate
    response = api_client.post('/api/v1/superdomains', headers=auth_headers, json={
        'name': 'UniqueTest',
        'description': 'Duplicate'
    })

    # Should return 400 Bad Request (unique constraint violation)
    assert response.status_code == 400


def test_create_superdomain_requires_auth(api_client):
    """Test POST /superdomains without auth returns 401."""
    response = api_client.post('/api/v1/superdomains', json={
        'name': 'Test',
        'description': 'Test'
    })

    # Should return 401 Unauthorized
    assert response.status_code == 401

"""Contract test for POST /domains endpoint.

Validates DomainCreate schema with superdomainId.
Expected to FAIL until implementation (TDD).
"""
import pytest


def test_create_domain_success(api_client, auth_headers, sample_superdomain_id):
    """Test POST /domains creates domain and returns 201."""
    response = api_client.post('/api/v1/domains', headers=auth_headers, json={
        'superdomainId': sample_superdomain_id,
        'name': 'Sales',
        'description': 'Sales and customer management'
    })

    # Should return 201 Created
    assert response.status_code == 201
    assert response.content_type == 'application/json'

    # Validate response matches Domain schema
    data = response.json
    assert 'id' in data
    assert 'superdomainId' in data
    assert 'name' in data
    assert 'description' in data
    assert 'createdAt' in data
    assert 'updatedAt' in data

    # Validate values
    assert data['superdomainId'] == sample_superdomain_id
    assert data['name'] == 'Sales'
    assert data['description'] == 'Sales and customer management'


def test_create_domain_missing_superdomain_id_returns_400(api_client, auth_headers):
    """Test POST /domains without required superdomainId returns 400."""
    response = api_client.post('/api/v1/domains', headers=auth_headers, json={
        'name': 'Sales',
        'description': 'Missing superdomain'
    })

    # Should return 400 Bad Request
    assert response.status_code == 400


def test_create_domain_missing_name_returns_400(api_client, auth_headers, sample_superdomain_id):
    """Test POST /domains without required name returns 400."""
    response = api_client.post('/api/v1/domains', headers=auth_headers, json={
        'superdomainId': sample_superdomain_id,
        'description': 'Missing name'
    })

    # Should return 400 Bad Request
    assert response.status_code == 400


def test_create_domain_invalid_superdomain_id_returns_400(api_client, auth_headers):
    """Test POST /domains with non-existent superdomainId returns 400."""
    response = api_client.post('/api/v1/domains', headers=auth_headers, json={
        'superdomainId': 99999,
        'name': 'Sales',
        'description': 'Invalid parent'
    })

    # Should return 400 Bad Request (foreign key constraint)
    assert response.status_code == 400


def test_create_domain_duplicate_name_in_superdomain_returns_400(api_client, auth_headers, sample_superdomain_id):
    """Test POST /domains with duplicate name in same superdomain returns 400."""
    # Create first domain
    api_client.post('/api/v1/domains', headers=auth_headers, json={
        'superdomainId': sample_superdomain_id,
        'name': 'UniqueDomain',
        'description': 'First'
    })

    # Try to create duplicate in same superdomain
    response = api_client.post('/api/v1/domains', headers=auth_headers, json={
        'superdomainId': sample_superdomain_id,
        'name': 'UniqueDomain',
        'description': 'Duplicate'
    })

    # Should return 400 Bad Request (unique constraint: superdomain_id, name)
    assert response.status_code == 400


def test_create_domain_requires_auth(api_client, sample_superdomain_id):
    """Test POST /domains without auth returns 401."""
    response = api_client.post('/api/v1/domains', json={
        'superdomainId': sample_superdomain_id,
        'name': 'Sales'
    })

    # Should return 401 Unauthorized
    assert response.status_code == 401

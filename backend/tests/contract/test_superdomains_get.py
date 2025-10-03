"""Contract test for GET /superdomains/{id} endpoint.

Validates Superdomain schema and 404 handling.
Expected to FAIL until implementation (TDD).
"""
import pytest


def test_get_superdomain_by_id_success(api_client, auth_headers, sample_superdomain_id):
    """Test GET /superdomains/{id} returns superdomain details."""
    response = api_client.get(
        f'/api/v1/superdomains/{sample_superdomain_id}',
        headers=auth_headers
    )

    # Should return 200 OK
    assert response.status_code == 200
    assert response.content_type == 'application/json'

    # Validate response matches Superdomain schema
    data = response.json
    assert 'id' in data
    assert 'name' in data
    assert 'description' in data
    assert 'createdAt' in data
    assert 'updatedAt' in data
    assert 'createdBy' in data

    # Validate types
    assert isinstance(data['id'], int)
    assert isinstance(data['name'], str)
    assert data['id'] == sample_superdomain_id


def test_get_superdomain_not_found_returns_404(api_client, auth_headers):
    """Test GET /superdomains/{id} with invalid ID returns 404."""
    response = api_client.get('/api/v1/superdomains/99999', headers=auth_headers)

    # Should return 404 Not Found
    assert response.status_code == 404
    assert response.content_type == 'application/json'

    # Should have error message
    data = response.json
    assert 'error' in data or 'message' in data


def test_get_superdomain_requires_auth(api_client, sample_superdomain_id):
    """Test GET /superdomains/{id} without auth returns 401."""
    response = api_client.get(f'/api/v1/superdomains/{sample_superdomain_id}')

    # Should return 401 Unauthorized
    assert response.status_code == 401


def test_get_superdomain_invalid_id_format_returns_400(api_client, auth_headers):
    """Test GET /superdomains/{id} with invalid ID format returns 400."""
    response = api_client.get('/api/v1/superdomains/invalid', headers=auth_headers)

    # Should return 400 Bad Request or 404 (depending on routing)
    assert response.status_code in [400, 404]

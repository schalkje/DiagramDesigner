"""Contract test for PUT /superdomains/{id} endpoint.

Validates SuperdomainUpdate schema.
Expected to FAIL until implementation (TDD).
"""
import pytest


def test_update_superdomain_success(api_client, auth_headers, sample_superdomain_id):
    """Test PUT /superdomains/{id} updates superdomain."""
    response = api_client.put(
        f'/api/v1/superdomains/{sample_superdomain_id}',
        headers=auth_headers,
        json={
            'name': 'Updated Business',
            'description': 'Updated description'
        }
    )

    # Should return 200 OK
    assert response.status_code == 200
    assert response.content_type == 'application/json'

    # Validate response matches Superdomain schema
    data = response.json
    assert 'id' in data
    assert 'name' in data
    assert 'description' in data
    assert data['name'] == 'Updated Business'
    assert data['description'] == 'Updated description'


def test_update_superdomain_partial_update(api_client, auth_headers, sample_superdomain_id):
    """Test PUT /superdomains/{id} with partial update (only name)."""
    response = api_client.put(
        f'/api/v1/superdomains/{sample_superdomain_id}',
        headers=auth_headers,
        json={'name': 'Only Name Updated'}
    )

    # Should return 200 OK
    assert response.status_code == 200
    data = response.json
    assert data['name'] == 'Only Name Updated'


def test_update_superdomain_not_found_returns_404(api_client, auth_headers):
    """Test PUT /superdomains/{id} with invalid ID returns 404."""
    response = api_client.put(
        '/api/v1/superdomains/99999',
        headers=auth_headers,
        json={'name': 'Test'}
    )

    # Should return 404 Not Found
    assert response.status_code == 404


def test_update_superdomain_name_too_long_returns_400(api_client, auth_headers, sample_superdomain_id):
    """Test PUT /superdomains/{id} with name >100 chars returns 400."""
    response = api_client.put(
        f'/api/v1/superdomains/{sample_superdomain_id}',
        headers=auth_headers,
        json={'name': 'x' * 101}
    )

    # Should return 400 Bad Request
    assert response.status_code == 400


def test_update_superdomain_requires_auth(api_client, sample_superdomain_id):
    """Test PUT /superdomains/{id} without auth returns 401."""
    response = api_client.put(
        f'/api/v1/superdomains/{sample_superdomain_id}',
        json={'name': 'Test'}
    )

    # Should return 401 Unauthorized
    assert response.status_code == 401

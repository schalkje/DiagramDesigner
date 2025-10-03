"""Contract test for DELETE /superdomains/{id} endpoint.

Validates DeleteImpact schema and cascade behavior.
Expected to FAIL until implementation (TDD).
"""
import pytest


def test_delete_superdomain_success(api_client, auth_headers, sample_superdomain_id):
    """Test DELETE /superdomains/{id} returns impact report."""
    response = api_client.delete(
        f'/api/v1/superdomains/{sample_superdomain_id}',
        headers=auth_headers
    )

    # Should return 200 OK (with impact report)
    assert response.status_code == 200
    assert response.content_type == 'application/json'

    # Validate response matches DeleteImpact schema
    data = response.json
    assert 'message' in data
    assert 'cascade' in data

    # Optional fields based on impact
    if 'affectedDiagrams' in data:
        assert isinstance(data['affectedDiagrams'], list)
    if 'affectedEntities' in data:
        assert isinstance(data['affectedEntities'], list)


def test_delete_superdomain_with_children_shows_impact(api_client, auth_headers):
    """Test DELETE on superdomain with domains shows affected entities."""
    # This test validates that cascade delete impact is reported
    # Actual cascade behavior tested in integration tests

    # Create superdomain with child domain
    sd_response = api_client.post('/api/v1/superdomains', headers=auth_headers, json={
        'name': 'TestDelete',
        'description': 'For deletion test'
    })
    superdomain_id = sd_response.json['id']

    # Create domain under it
    api_client.post('/api/v1/domains', headers=auth_headers, json={
        'superdomainId': superdomain_id,
        'name': 'ChildDomain',
        'description': 'Will be affected'
    })

    # Delete superdomain
    response = api_client.delete(
        f'/api/v1/superdomains/{superdomain_id}',
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json
    assert data['cascade'] is True  # Should indicate cascade delete
    assert 'affectedEntities' in data or 'message' in data


def test_delete_superdomain_not_found_returns_404(api_client, auth_headers):
    """Test DELETE /superdomains/{id} with invalid ID returns 404."""
    response = api_client.delete('/api/v1/superdomains/99999', headers=auth_headers)

    # Should return 404 Not Found
    assert response.status_code == 404


def test_delete_superdomain_requires_auth(api_client, sample_superdomain_id):
    """Test DELETE /superdomains/{id} without auth returns 401."""
    response = api_client.delete(f'/api/v1/superdomains/{sample_superdomain_id}')

    # Should return 401 Unauthorized
    assert response.status_code == 401

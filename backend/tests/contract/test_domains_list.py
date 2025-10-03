"""Contract test for GET /domains endpoint.

Validates filtering by superdomainId and Domain schema.
Expected to FAIL until implementation (TDD).
"""
import pytest


def test_list_domains_returns_paginated_data(api_client, auth_headers):
    """Test GET /domains returns paginated list."""
    response = api_client.get('/api/v1/domains', headers=auth_headers)

    # Should return 200 OK
    assert response.status_code == 200
    assert response.content_type == 'application/json'

    # Validate response structure
    data = response.json
    assert 'data' in data
    assert 'pagination' in data
    assert isinstance(data['data'], list)


def test_list_domains_filter_by_superdomain_id(api_client, auth_headers, sample_superdomain_id):
    """Test GET /domains with superdomainId filter."""
    response = api_client.get(
        f'/api/v1/domains?superdomainId={sample_superdomain_id}',
        headers=auth_headers
    )

    # Should return 200 OK
    assert response.status_code == 200
    data = response.json

    # All returned domains should belong to specified superdomain
    for domain in data['data']:
        assert 'superdomainId' in domain
        assert domain['superdomainId'] == sample_superdomain_id


def test_list_domains_validates_domain_schema(api_client, auth_headers):
    """Test domain objects match OpenAPI Domain schema."""
    response = api_client.get('/api/v1/domains', headers=auth_headers)

    assert response.status_code == 200
    data = response.json

    if len(data['data']) > 0:
        domain = data['data'][0]
        assert 'id' in domain
        assert 'superdomainId' in domain
        assert 'name' in domain
        assert 'createdAt' in domain
        assert 'updatedAt' in domain

        # Validate types
        assert isinstance(domain['id'], int)
        assert isinstance(domain['superdomainId'], int)
        assert isinstance(domain['name'], str)


def test_list_domains_requires_auth(api_client):
    """Test GET /domains without auth returns 401."""
    response = api_client.get('/api/v1/domains')

    assert response.status_code == 401

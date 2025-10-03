"""Contract test for GET /superdomains endpoint.

Validates pagination schema and list response structure.
Expected to FAIL until implementation (TDD).
"""
import pytest


def test_list_superdomains_returns_paginated_data(api_client, auth_headers):
    """Test GET /superdomains returns paginated list."""
    response = api_client.get('/api/v1/superdomains', headers=auth_headers)

    # Should return 200 OK
    assert response.status_code == 200
    assert response.content_type == 'application/json'

    # Validate response structure matches OpenAPI spec
    data = response.json
    assert 'data' in data, "Response must include 'data' array"
    assert 'pagination' in data, "Response must include 'pagination' object"

    # Validate data is an array
    assert isinstance(data['data'], list)

    # Validate pagination object structure
    pagination = data['pagination']
    assert 'page' in pagination
    assert 'pageSize' in pagination
    assert 'total' in pagination
    assert 'totalPages' in pagination

    # Validate pagination types
    assert isinstance(pagination['page'], int)
    assert isinstance(pagination['pageSize'], int)
    assert isinstance(pagination['total'], int)
    assert isinstance(pagination['totalPages'], int)


def test_list_superdomains_with_page_param(api_client, auth_headers):
    """Test GET /superdomains with page parameter."""
    response = api_client.get('/api/v1/superdomains?page=2', headers=auth_headers)

    assert response.status_code == 200
    data = response.json
    assert data['pagination']['page'] == 2


def test_list_superdomains_with_pagesize_param(api_client, auth_headers):
    """Test GET /superdomains with pageSize parameter."""
    response = api_client.get('/api/v1/superdomains?pageSize=50', headers=auth_headers)

    assert response.status_code == 200
    data = response.json
    assert data['pagination']['pageSize'] == 50


def test_list_superdomains_requires_auth(api_client):
    """Test GET /superdomains without auth returns 401."""
    response = api_client.get('/api/v1/superdomains')

    # Should return 401 Unauthorized
    assert response.status_code == 401


def test_list_superdomains_validates_superdomain_schema(api_client, auth_headers):
    """Test that superdomain objects match OpenAPI schema."""
    response = api_client.get('/api/v1/superdomains', headers=auth_headers)

    assert response.status_code == 200
    data = response.json

    # If there are superdomains, validate their structure
    if len(data['data']) > 0:
        superdomain = data['data'][0]
        assert 'id' in superdomain
        assert 'name' in superdomain
        assert 'createdAt' in superdomain
        assert 'updatedAt' in superdomain

        # Validate types
        assert isinstance(superdomain['id'], int)
        assert isinstance(superdomain['name'], str)

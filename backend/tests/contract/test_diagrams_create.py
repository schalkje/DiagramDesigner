"""Contract test for POST /diagrams endpoint.

Validates DiagramCreate schema with tags array.
Expected to FAIL until implementation (TDD).
"""
import pytest


def test_create_diagram_success(api_client, auth_headers):
    """Test POST /diagrams creates diagram and returns 201."""
    response = api_client.post('/api/v1/diagrams', headers=auth_headers, json={
        'name': 'Sales Overview',
        'description': 'Overview of sales data model',
        'purpose': 'Show customer and order relationships',
        'tags': ['sales', 'customer', 'overview']
    })

    # Should return 201 Created
    assert response.status_code == 201
    assert response.content_type == 'application/json'

    # Validate response matches Diagram schema
    data = response.json
    assert 'id' in data
    assert 'name' in data
    assert 'description' in data
    assert 'purpose' in data
    assert 'tags' in data
    assert 'canvasSettings' in data or data.get('canvasSettings') is None
    assert 'objects' in data
    assert 'relationships' in data
    assert 'createdAt' in data
    assert 'updatedAt' in data

    # Validate values
    assert data['name'] == 'Sales Overview'
    assert data['description'] == 'Overview of sales data model'
    assert isinstance(data['tags'], list)
    assert len(data['tags']) == 3
    assert 'sales' in data['tags']


def test_create_diagram_missing_name_returns_400(api_client, auth_headers):
    """Test POST /diagrams without required name returns 400."""
    response = api_client.post('/api/v1/diagrams', headers=auth_headers, json={
        'description': 'Missing name',
        'tags': []
    })

    # Should return 400 Bad Request
    assert response.status_code == 400


def test_create_diagram_name_too_long_returns_400(api_client, auth_headers):
    """Test POST /diagrams with name >100 chars returns 400."""
    response = api_client.post('/api/v1/diagrams', headers=auth_headers, json={
        'name': 'x' * 101,
        'description': 'Test'
    })

    # Should return 400 Bad Request (maxLength: 100)
    assert response.status_code == 400


def test_create_diagram_minimal_fields(api_client, auth_headers):
    """Test POST /diagrams with only required name field."""
    response = api_client.post('/api/v1/diagrams', headers=auth_headers, json={
        'name': 'Minimal Diagram'
    })

    # Should return 201 Created (other fields optional)
    assert response.status_code == 201
    data = response.json
    assert data['name'] == 'Minimal Diagram'
    # Optional fields may be null or have default values
    assert 'tags' in data


def test_create_diagram_with_empty_tags_array(api_client, auth_headers):
    """Test POST /diagrams with empty tags array."""
    response = api_client.post('/api/v1/diagrams', headers=auth_headers, json={
        'name': 'No Tags',
        'tags': []
    })

    # Should return 201 Created
    assert response.status_code == 201
    data = response.json
    assert isinstance(data['tags'], list)
    assert len(data['tags']) == 0


def test_create_diagram_with_multiple_tags(api_client, auth_headers):
    """Test POST /diagrams with multiple tags."""
    tags = ['tag1', 'tag2', 'tag3', 'tag4', 'tag5']
    response = api_client.post('/api/v1/diagrams', headers=auth_headers, json={
        'name': 'Multi-Tag Diagram',
        'tags': tags
    })

    # Should return 201 Created
    assert response.status_code == 201
    data = response.json
    assert len(data['tags']) == 5
    for tag in tags:
        assert tag in data['tags']


def test_create_diagram_validates_tags_is_array(api_client, auth_headers):
    """Test POST /diagrams with tags as non-array returns 400."""
    response = api_client.post('/api/v1/diagrams', headers=auth_headers, json={
        'name': 'Invalid Tags',
        'tags': 'not_an_array'
    })

    # Should return 400 Bad Request (tags must be array)
    assert response.status_code == 400


def test_create_diagram_returns_empty_objects_array(api_client, auth_headers):
    """Test POST /diagrams returns empty objects and relationships arrays."""
    response = api_client.post('/api/v1/diagrams', headers=auth_headers, json={
        'name': 'New Diagram'
    })

    # Should return 201 Created
    assert response.status_code == 201
    data = response.json

    # New diagram should have empty objects and relationships
    assert 'objects' in data
    assert isinstance(data['objects'], list)
    assert len(data['objects']) == 0

    assert 'relationships' in data
    assert isinstance(data['relationships'], list)
    assert len(data['relationships']) == 0


def test_create_diagram_requires_auth(api_client):
    """Test POST /diagrams without auth returns 401."""
    response = api_client.post('/api/v1/diagrams', json={
        'name': 'Test Diagram'
    })

    # Should return 401 Unauthorized
    assert response.status_code == 401

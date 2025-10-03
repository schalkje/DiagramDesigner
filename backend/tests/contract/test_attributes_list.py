"""Contract test for GET /entities/{entityId}/attributes endpoint.

Validates Attribute schema.
Expected to FAIL until implementation (TDD).
"""
import pytest


def test_list_attributes_for_entity(api_client, auth_headers, sample_entity_id):
    """Test GET /entities/{entityId}/attributes returns attribute list."""
    response = api_client.get(
        f'/api/v1/entities/{sample_entity_id}/attributes',
        headers=auth_headers
    )

    # Should return 200 OK
    assert response.status_code == 200
    assert response.content_type == 'application/json'

    # Validate response structure
    data = response.json
    assert 'data' in data
    assert isinstance(data['data'], list)


def test_list_attributes_validates_attribute_schema(api_client, auth_headers, sample_entity_id):
    """Test attribute objects match OpenAPI Attribute schema."""
    response = api_client.get(
        f'/api/v1/entities/{sample_entity_id}/attributes',
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json

    if len(data['data']) > 0:
        attribute = data['data'][0]
        assert 'id' in attribute
        assert 'entityId' in attribute
        assert 'name' in attribute
        assert 'dataType' in attribute
        assert 'isNullable' in attribute
        assert 'createdAt' in attribute
        assert 'updatedAt' in attribute

        # Validate types
        assert isinstance(attribute['id'], int)
        assert isinstance(attribute['entityId'], int)
        assert isinstance(attribute['name'], str)
        assert isinstance(attribute['dataType'], str)
        assert isinstance(attribute['isNullable'], bool)

        # Validate dataType is from allowed enum
        valid_types = [
            'String', 'Text', 'Integer', 'BigInteger', 'Float', 'Decimal',
            'Boolean', 'Date', 'DateTime', 'Time', 'UUID', 'JSON'
        ]
        assert attribute['dataType'] in valid_types


def test_list_attributes_invalid_entity_returns_404(api_client, auth_headers):
    """Test GET /entities/{entityId}/attributes with invalid entity returns 404."""
    response = api_client.get('/api/v1/entities/99999/attributes', headers=auth_headers)

    # Should return 404 Not Found
    assert response.status_code == 404


def test_list_attributes_requires_auth(api_client, sample_entity_id):
    """Test GET /entities/{entityId}/attributes without auth returns 401."""
    response = api_client.get(f'/api/v1/entities/{sample_entity_id}/attributes')

    assert response.status_code == 401
